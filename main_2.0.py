from registry import get_packages

from fetchers.github_v2 import GitHubFetcher
from fetchers.index_fetcher_v2 import IndexFetcher
from fetchers.pypi_fetcher import PyPIFetcher
from fetchers.sourceforge_fetcher import SourceForgeFetcher

from downloaders.directory import DirectoryManager
from downloaders.downloader_v2 import Downloader


FETCHERS = {
    "IndexFetcher": IndexFetcher,
    "GitHubFetcher": GitHubFetcher,
    "PyPIFetcher": PyPIFetcher,
    "SourceForgeFetcher": SourceForgeFetcher,
}


packages = get_packages()

downloader = Downloader()
directory_manager = DirectoryManager()

for package in packages:

    print("=" * 60)
    print(package["package_name"])

    try:

        fetcher = FETCHERS[package["fetcher"]](package)

        assets = fetcher.discover()

        version = (
            package["download_url"]
            .split("/")[-1]
            .split(".tar")[0]
        )

        version_directory = directory_manager.create_version(
            package["package_name"],
            version,
        )

        for name, url in assets.items():

            downloader.download(
                {
                    "name": name,
                    "url": url,
                },
                output_directory=version_directory,
            )

        print()

    except Exception as e:

        with open("errors_2.log", "a") as f:

            f.write(
                f"[ERROR] "
                f"{package['package_name']} "
                f"({package['fetcher']}): "
                f"({package['download_url']}) "
                f"{e}\n"
            )

        print(f"[ERROR] {e}")