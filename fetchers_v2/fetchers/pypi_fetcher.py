import requests


class PyPIFetcher:

    def __init__(self, package):
        self.package = package

    def discover(self):

        filename = self.package["download_url"].split("/")[-1]

        return {
            filename: self.package["download_url"]
        }