from pathlib import Path


class DirectoryCreator:

    @staticmethod
    def create(*paths):

        path = Path(*paths)

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        print(f"Creating directory: {path}")

        return path