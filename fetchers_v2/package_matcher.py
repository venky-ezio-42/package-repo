class PackageMatcher:

    @staticmethod
    def matches(
        prefix: str,
        filename: str,
    ) -> bool:

        return filename.startswith(prefix)