import csv
import tldextract
import functools


class Whitelist:
    """ Represents a set of urls that are whitelisted """

    def __init__(self):
        self.domain_set = set()

    def load(self, csv_path):
        with open(csv_path, newline="") as f:
            reader = csv.reader(f)
            for r in reader:
                self.domain_set.add(r[-1])

    @functools.cache
    def contains_url(self, url):
        # get domain from url
        extract = tldextract.extract(url)
        tld = ".".join([l for l in [extract.domain, extract.suffix] if len(l) > 0])
        print(f"TLD - {tld}")

        # lookup if in whitelist
        return tld in self.domain_set