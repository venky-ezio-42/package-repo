import requests

from fetchers_v2.downloader import Downloader
from fetchers_v2.version_extractor import VersionExtractor
from fetchers_v2.version_selector import VersionSelector
from fetchers_v2.package_matcher import PackageMatcher


class GitHubFetcher:

    ARCHIVE_EXTENSIONS = (
        ".tar.gz",
        ".tar.xz",
        ".tar.bz2",
        ".tgz",
    )

    SIGNATURE_EXTENSIONS = (
        ".asc",
        ".sig",
    )

    def __init__(self, package):

        self.package = package

        self.repo_url = package["source_url"]

        self.prefix = package["package_prefix"]
        self.version_type = package["version_type"]
        self.major_version = package.get("major_version")

        self.session = requests.Session()

        self.api_url = self._get_api_url(
            self.repo_url
        )

    def _get_api_url(self, repo_url):

        parts = repo_url.rstrip("/").split("/")

        if len(parts) < 2:
            raise ValueError(
                f"Invalid GitHub repository URL: {repo_url}"
            )

        owner = parts[-2]
        repo = parts[-1]

        return (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}"
        )

    def get_releases(self):

        releases = []

        page = 1

        while True:

            response = self.session.get(
                f"{self.api_url}/releases",
                params={
                    "per_page": 100,
                    "page": page,
                },
                timeout=30,
            )

            response.raise_for_status()

            page_releases = response.json()

            if not page_releases:
                break

            releases.extend(
                page_releases
            )

            if len(page_releases) < 100:
                break

            page += 1

        return releases

    def get_version(self, tag):

        try:

            return VersionExtractor.extract_version(
                filename=tag,
                version_type=self.version_type,
            )

        except ValueError as e:

            print(
                f"[FAILED] "
                f"{tag} -> {e}"
            )

            return None

    def allowed_version(self, version):

        if not self.major_version:
            return True

        return VersionSelector.belongs_to_major(
            version,
            self.version_type,
            self.major_version,
        )

    def is_archive(self, filename):

        return filename.endswith(
            self.ARCHIVE_EXTENSIONS
        )

    def is_signature(self, filename):

        return filename.endswith(
            self.SIGNATURE_EXTENSIONS
        )

    def is_allowed_asset(self, filename):

        return (
            self.is_archive(filename)
            or
            self.is_signature(filename)
        )

    def discover(self):

        releases = self.get_releases()

        assets = []

        print(
            f"[INFO] Found {len(releases)} "
            f"GitHub releases"
        )

        for release in releases:

            tag = release.get(
                "tag_name"
            )

            if not tag:
                continue

            version = self.get_version(
                tag
            )

            if version is None:
                continue

            if not self.allowed_version(
                version
            ):
                continue

            print(
                f"\nRELEASE : {tag}"
            )

            for asset in release.get(
                "assets",
                []
            ):

                name = asset.get(
                    "name"
                )

                url = asset.get(
                    "browser_download_url"
                )

                if not name or not url:
                    continue

                #
                # Only source archives/signatures
                #
                if not self.is_allowed_asset(
                    name
                ):
                    continue

                #
                # Package match
                #
                if not PackageMatcher.matches(
                    self.prefix,
                    name,
                ):

                    continue

                assets.append(
                    {
                        "name": name,
                        "url": url,
                        "version": version,
                    }
                )

                print(
                    f"  -> {name}"
                )

        print(
            f"\n[INFO] Found {len(assets)} "
            f"assets for "
            f"{self.package['package_name']}"
        )

        #
        # Create directories after discovery
        #
        for asset in assets:

            asset["directory"] = (
                VersionExtractor.create_version_directory(
                    package_name=self.package[
                        "package_name"
                    ],
                    version=asset["version"],
                    version_type=self.version_type,
                )
            )

        return assets
