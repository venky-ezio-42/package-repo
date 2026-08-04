from downloaders.directory import DirectoryManager
from downloaders.download import Downloader

from registry import get_packages

from fetchers.index import IndexFetcher
from fetchers.github import GitHubFetcher



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


    fetcher_name = package["fetcher"]


    if fetcher_name not in FETCHERS:

        print(
            f"[SKIP] {package['package_name']} "
            f"({fetcher_name})"
        )

        continue



    print("=" * 60)

    print(
        package["package_name"]
    )


    fetcher = FETCHERS[fetcher_name](
        package
    )


    try:


        releases = fetcher.fetch_releases()



        for release in releases:


            print(
                f"Version : {release['version']}"
            )

            print(
                f"Published : {release['published']}"
            )


            version_directory = (
                directory_manager.create_version(
                    package["package_name"],
                    release["version"]
                )
            )


            downloader.download(
                assets=release["assets"],
                destination=version_directory
            )



            for asset in release["assets"]:

                print(
                    "  ",
                    asset["name"]
                )


            print()



    except Exception as e:


        with open(
            "errors.log",
            "a"
        ) as f:

            f.write(
                f"[ERROR] "
                f"{package['package_name']} "
                f"({fetcher_name}): "
                f"{package['source_url']} "
                f"{e}\n"
            )


        print(
            f"[ERROR] {e}"
        )