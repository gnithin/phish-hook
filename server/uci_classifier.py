import datetime
import os
import socket
from urllib.parse import urlparse

import numpy as np
import requests
import whois
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from joblib import load
from typing import List
from abstract_classifier import AbstractClassifier


class UciClassifier(AbstractClassifier):
    PHISHING = -1
    SUSPICIOUS = 0
    LEGITIMATE = 1
    shorteners = set(
        line.strip() for line in open(os.path.join("assets", "shorteners.txt"))
    )
    ccTLDs = set(line.strip() for line in open(os.path.join("assets", "ccTLD.txt")))

    def __init__(self, model_path: str):
        load_dotenv()
        if os.getenv("PR_API") is None:
            raise ValueError(
                "PR_API environment variable not set. Check your .env file"
            )
        self.classifier = load(model_path)

    def has_ip_address(self, netloc: str) -> int:
        if netloc[0].isnumeric():
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def url_length(self, url: str) -> int:
        length = len(url)
        if length < 54:
            return self.LEGITIMATE
        elif 54 <= length <= 75:
            return self.SUSPICIOUS
        else:
            return self.PHISHING

    def using_shortener(self, netloc: str) -> int:
        if netloc in self.shorteners:
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def has_at_symbol(self, url: str) -> int:
        if "@" in url:
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def has_double_slash(self, url: str) -> int:
        if url.rfind("//") > 7:
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def has_dash_symbol(self, url: str) -> int:
        if "-" in url:
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def sub_domains(self, netloc: str) -> int:
        split = netloc.split(".")
        if split[-1] in self.ccTLDs:
            del split[-1]
        if split[0] == "www":
            del split[0]

        if len(split) == 2:
            return self.LEGITIMATE
        elif len(split) == 3:
            return self.SUSPICIOUS
        else:
            return self.PHISHING

    def domain_expiration(self, netloc: str) -> int:
        expiration = whois.whois(netloc).expiration_date
        if expiration is None:
            return self.PHISHING

        now = datetime.datetime.now()
        if isinstance(expiration, datetime.datetime):
            delta = [relativedelta(expiration, now).years > 1]
        elif isinstance(expiration, list):
            delta = map(lambda exp: relativedelta(exp, now).years > 1, expiration)
        else:
            return self.PHISHING

        if any(delta):
            return self.LEGITIMATE
        else:
            return self.PHISHING

    @staticmethod
    def __is_port_open(host, port):
        captive_dns_addr = ""
        try:
            captive_dns_addr = socket.gethostbyname("BlahThisDomaynDontExist22.com")
        except:
            pass

        try:
            host_addr = socket.gethostbyname(host)

            if captive_dns_addr == host_addr:
                return False

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            s.close()
        except:
            return False

        return True

    def check_ports(self, netloc: str) -> int:
        closed_ports = [21, 22, 23, 445, 1433, 1521, 3306, 3389]
        all_closed = any(
            map(lambda x: not self.__is_port_open(netloc, x), closed_ports)
        )

        open_ports = [80, 443]
        all_open = all(map(lambda x: self.__is_port_open(netloc, x), open_ports))

        if all_open and all_closed:
            return self.LEGITIMATE
        else:
            return self.PHISHING

    def https_in_domain(self, netloc: str) -> int:
        if "https" in netloc.lower():
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def domain_age(self, netloc: str) -> int:
        creation = whois.whois(netloc).creation_date

        if creation is None:
            return self.PHISHING
        now = datetime.datetime.now()
        if isinstance(creation, datetime.datetime):
            delta = [relativedelta(creation, now).years > 1]
        elif isinstance(creation, list):
            delta = map(lambda c: relativedelta(now, c), creation)
            delta = map(lambda c: c.years < 0 and c.months <= 6, delta)
        else:
            return self.PHISHING

        if all(delta):
            return self.PHISHING
        else:
            return self.LEGITIMATE

    def page_rank(self, netloc: str) -> int:
        url = "https://openpagerank.com/api/v1.0/getPageRank"
        params = {"domains[]": netloc}

        r = requests.get(
            url=url, params=params, headers={"API-OPR": os.getenv("PR_API")}
        )

        data = r.json()
        page_rank = data["response"][0]["page_rank_decimal"]

        # Handling the weird case when the response is a string
        if isinstance(page_rank, str):
            try:
                page_rank = int(page_rank)
            except:
                page_rank = None

        if page_rank is not None and page_rank >= 2:
            return self.LEGITIMATE
        else:
            return self.PHISHING

    def get_feature_list(self, url: str) -> List[int]:
        # scheme://netloc/path;parameters?query#fragment.
        parsed = urlparse(url)
        netloc = parsed.netloc
        if parsed.scheme == "":
            url = "http://" + url
            parsed = urlparse(url)
            netloc = parsed.netloc

        features = list()
        features.append(self.has_ip_address(netloc))
        features.append(self.url_length(url))
        features.append(self.using_shortener(netloc))
        features.append(self.has_at_symbol(url))
        features.append(self.has_double_slash(url))
        features.append(self.has_dash_symbol(url))
        features.append(self.sub_domains(netloc))
        features.append(self.domain_expiration(netloc))
        features.append(self.check_ports(netloc))
        features.append(self.https_in_domain(netloc))
        features.append(self.domain_age(netloc))
        features.append(self.page_rank(netloc))

        return features

    def is_phishing(self, url: str) -> bool:
        features = self.get_feature_list(url)
        arr = np.array(features).reshape(1, -1)

        prediction = self.classifier.predict(arr)

        if prediction[0] == 1:
            return False
        else:
            return True

    def predict(self, url) -> bool:
        return self.is_phishing(url)