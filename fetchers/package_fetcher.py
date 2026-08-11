import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from fetchers_v2.downloader import Downloader
from fetchers_v2.version_extractor import VersionExtractor
from fetchers_v2.version_selector import VersionSelector
from fetchers_v2.package_matcher import PackageMatcher


class IndexFetcher:

    ARCHIVE_EXTENSIONS = (
        ".tar.gz",
        ".tar.xz",
        ".tar.bz2",
        ".tgz",
        ".zip",
        ".gpg",
        ".tar.gz.asc",
        ".tar.xz.asc",
        ".tar.bz2.asc",
        ".tgz.asc.sig",
        ".tar.gz.sig",
        ".tar.xz.sig",
        ".tar.bz2.sig",
        ".tgz.sig",
        ".tar.gz.sha256.txt",
        ".tar.xz.sha256.txt",
        ".tar.bz2.sha256.txt",
        ".tar.gz.md5.txt",
        ".tar.xz.md5.txt",
        ".tar.bz2.md5.txt",
    )

    def __init__(self, package):

        self.package = package

        self.source_url = package["source_url"]

        self.prefix = package["package_prefix"]
        self.version_type = package["version_type"]
        self.major_version = package.get("major_version")

        self.visited = set()

    def discover(self):

        assets = self.crawl(
            self.source_url
        )

        print(
            f"[INFO] Found {len(assets)} assets "
            f"for {self.package['package_name']}"
        )

        for asset in assets:

            version = asset["version"]

            directory = VersionExtractor.create_version_directory(
                package_name=self.package["package_name"],
                version=version,
                version_type=self.version_type,
            )

            asset["directory"] = directory

        return assets


    def is_archive(self, filename):

        return filename.endswith(
            self.ARCHIVE_EXTENSIONS
        )


    def extract_filename(self, href):

        return href.rstrip("/").split("/")[-1]


    def get_page(self, url):

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return BeautifulSoup(
            response.text,
            "html.parser"
        )


    def get_version(
        self,
        value,
        is_directory=False,
    ):

        try:

            return VersionExtractor.extract_version(
                filename=value,
                package_prefix=None if is_directory else self.prefix,
                version_type=self.version_type,
            )

        except ValueError as e:
            print(f"FAILED '{value}' -> {e}")
            return None


    def allowed_version(self, version):

        if not self.major_version:
            return True

        return VersionSelector.belongs_to_major(
            version,
            self.version_type,
            self.major_version,
        )
    
    KEY_EXTENSIONS = (
        ".gpg",
        ".pgp",
        ".key",
        ".asc",
    )
    
    def is_key_file(self, filename):

        lower = filename.lower()

        if not lower.endswith(self.KEY_EXTENSIONS):
            return False

        # Package signatures are handled as package assets
        if lower.endswith((
            ".tar.gz.asc",
            ".tar.xz.asc",
            ".tar.bz2.asc",
            ".tgz.asc",
        )):
            return False

        return True


    def crawl(self, url):

        print(f"\nCRAWLING: {url}")

        if url in self.visited:
            print("  -> already visited")
            return []

        self.visited.add(url)

        assets = []

        soup = self.get_page(url)

        for link in soup.find_all("a", href=True):

            href = link["href"]

            if href in ("../", "./"):
                continue

            full_url = urljoin(url, href)

            print(f"\nHREF : {href}")

            #
            # SOURCEFORGE DOWNLOAD LINK
            #
            if href.endswith("/download"):

                # print("  TYPE : download")

                filename = href.split("/")[-2]

                if not self.is_archive(filename):
                    continue

                # print(f"  FILE : {filename}")

                if not PackageMatcher.matches(
                    self.prefix,
                    filename,
                ):
                    # print("  -> package mismatch")
                    continue

                version = self.get_version(
                    filename
                )

                # print(f"  VERSION : {version}")

                if version is None:
                    # print("  -> invalid version")
                    continue

                if not self.allowed_version(
                    version
                ):
                    # print("  -> wrong major version")
                    continue

                # print("  -> ACCEPTED")

                assets.append(
                    {
                        "name": filename,
                        "url": full_url,
                        "version": version,
                    }
                )

                continue

            #
            # DIRECTORY
            #
            if href.endswith("/"):

                # print("  TYPE : directory")

                directory = href.rstrip("/").split("/")[-1]

                # print(f"  DIR : {directory}")

                directory_version = self.get_version(
                    directory,
                    is_directory=True
                )

                # print(f"  VERSION : {directory_version}")

                if directory_version is None:
                    # print("  -> not a version directory")
                    continue

                if not self.allowed_version(
                    directory_version
                ):
                    # print("  -> wrong major version")
                    continue

                print(f"  -> RECURSING INTO {full_url}")

                assets.extend(
                    self.crawl(full_url)
                )

                continue

            #
            # NORMAL FILE
            #
            # print("  TYPE : normal file")

            filename = self.extract_filename(
                href
            )

            # --------------------------------
            # KEY / GPG FILE
            # --------------------------------

            if self.is_key_file(filename):

                assets.append(
                    {
                        "name": filename,
                        "url": full_url,
                        "version": None,
                        "type": "key",
                    }
                )

                continue

            # print(f"  FILE : {filename}")

            if not self.is_archive(
                filename
            ):
                # print("  -> not archive")
                continue

            if not PackageMatcher.matches(
                self.prefix,
                filename,
            ):
                # print("  -> package mismatch")
                continue

            version = self.get_version(
                filename
            )

            # print(f"  VERSION : {version}")

            if version is None:
                # print("  -> invalid version")
                continue

            if not self.allowed_version(
                version
            ):
                # print("  -> wrong major version")
                continue

            # print("  -> ACCEPTED")

            
            assets.append(
                {
                    "name": filename,
                    "url": full_url,
                    "version": version,
                }
            )

        # print(f"\nLEAVING {url} ({len(assets)} assets)")
        # print(assets)

        return assets
    
    

