from fetchers.github_v2 import GitHubFetcher
from fetchers.package_fetcher import IndexFetcher


class FetcherFactory:

    @staticmethod
    def create(package):

        source_url = package[
            "source_url"
        ]

        if "github.com" in source_url:

            return GitHubFetcher(
                package
            )

        return IndexFetcher(
            package
        )
