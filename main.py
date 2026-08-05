from downloaders.directory import DirectoryManager
from downloaders.download import Downloader

from registry import get_packages

from fetchers.index import IndexFetcher
from fetchers.github import GitHubFetcher

import re


FETCHERS = {

    "IndexFetcher": IndexFetcher,
    "GitHubFetcher": GitHubFetcher,

}



directory_manager = DirectoryManager(
    "packages"
)

downloader = Downloader()


packages = get_packages()


for package in packages:

    print("=" * 60)

    print(
        package["package_name"]
    )

    try:

        if "github.com" in package["download_url"]:

            fetcher = GitHubFetcher(
                package
            )

        else:

            fetcher = IndexFetcher(
                package
            )


        assets = fetcher.discover()


        filename = (
            package["download_url"]
            .split("/")[-1]
        )

        version = re.sub(
            r"\.(tar\.gz|tar\.xz|tar\.bz2|tgz)$",
            "",
            filename
        )


        version_directory = (
            directory_manager.create_version(
                package["package_name"],
                version
            )
        )


        downloader.download(
            assets=assets,
            destination=version_directory
        )


        for asset in assets:

            print(
                "  ",
                asset["name"]
            )

        print()


    except Exception as e:

        with open(
            "errors_2.log",
            "a"
        ) as f:

            f.write(
                f"[ERROR] "
                f"{package['package_name']}: "
                f"{package['source_url']} "
                f"{e}\n"
            )

        print(
            f"[ERROR] {e}"
        )