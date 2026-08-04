from pathlib import Path


class DirectoryManager:

    def __init__(
        self,
        root_directory="packages"
    ):

        self.root = Path(root_directory)

        self.root.mkdir(
            parents=True,
            exist_ok=True
        )


    def get_package_directory(
        self,
        package_name
    ):

        path = self.root / package_name

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path



    def create_version(
        self,
        package_name,
        version
    ):

        package_path = self.get_package_directory(
            package_name
        )

        version_path = package_path / version

        version_path.mkdir(
            parents=True,
            exist_ok=True
        )

        return version_path