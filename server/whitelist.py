import csv
import tldextract


class Whitelist:
    def __init__(self):
        self.domain_set = set()

    def load(self, csv_path):
        with open(csv_path, newline="") as f:
            reader = csv.reader(f)
            for r in reader:
                self.domain_set.add(r[-1])

    def contains_url(self, url):
        # get domain from url
        extract = tldextract.extract(url)
        tld = f"{extract.domain}.{extract.suffix}"
        print(tld)

        # lookup if in whitelist
        return tld in self.domain_set