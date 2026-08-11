import re
from urllib.parse import urlparse

import requests


class GitHubFetcher:

    def __init__(self, package):

        self.package = package

        self.package_name = package["package_name"]
        self.source_url = package["source_url"]

        self.public_key_url = package.get("public_key_url")
        self.public_key_name = package.get("public_key_name")

        parts = urlparse(self.source_url).path.strip("/").split("/")

        if len(parts) < 2:
            raise ValueError(f"Invalid GitHub repository URL: {self.source_url}")

        self.owner = parts[0]
        self.repo = parts[1]

        self.api = (
            f"https://api.github.com/repos/"
            f"{self.owner}/{self.repo}/releases"
        )

    def discover(self):

        response = requests.get(
            self.api,
            headers={
                "Accept": "application/vnd.github+json"
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def fetch_releases(self, limit=2):

        parsed = []

        releases = self.discover()

        archive_regex = re.compile(
            r"\.(tar\.gz|tar\.xz|tar\.bz2|tgz)(?:\.(asc|sig))?$"
        )

        for release in releases[:limit]:

            assets = []

            for asset in release["assets"]:

                name = asset["name"]

                if name.startswith("Source code"):
                    continue

                if not archive_regex.search(name):
                    continue

                assets.append(
                    {
                        "name": name,
                        "url": asset["browser_download_url"],
                        "digest": asset.get("digest"),
                        "size": asset["size"],
                    }
                )

            parsed.append(
                {
                    "package": self.package_name,
                    "version": release["tag_name"],
                    "published": release["published_at"],
                    "assets": assets,
                }
            )

        return parsed

    def get_public_key_url(self):
        return self.public_key_url

    def get_public_key_name(self):
        return self.public_key_name