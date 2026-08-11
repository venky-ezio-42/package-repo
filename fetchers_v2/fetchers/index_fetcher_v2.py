from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import re

class IndexFetcher:

    def __init__(self, package):
        self.package = package
        self.download_url = package["download_url"]
        self.source_url = package["source_url"]

    def discover(self):

        listing_url = self.source_url.rsplit("/", 1)[0] + "/"

        r = requests.get(listing_url, timeout=30)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        assets = {}

        wanted = self.package["download_url"].split("/")[-1]

        print("WANTED PACKAGE ", wanted)

        for a in soup.find_all("a", href=True):

            href = a["href"]
            filename = href.split("/")[-1]

            if filename == wanted:
                assets[filename] = urljoin(listing_url, href)

            elif filename in (
                wanted + ".asc",
                wanted + ".sig",
                wanted + ".sign",
                wanted + ".crt",
            ):
                assets[filename] = urljoin(listing_url, href)

        print(f"[INFO] Discovered {len(assets)} assets for {self.package['package_name']}")
        print(f"[INFO] Assets: {list(assets.keys())}")
        
        return assets