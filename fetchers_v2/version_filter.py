from fetchers_v2.version_selector import VersionSelector


class VersionFilter:

    @staticmethod
    def filter(
        assets,
        version_type,
        major_version,
    ):

        if not major_version:

            return assets

        filtered = []

        for asset in assets:

            version = asset.get(
                "version"
            )

            if version is None:
                continue

            if VersionSelector.belongs_to_major(
                version,
                version_type,
                major_version,
            ):

                filtered.append(
                    asset
                )

        return filtered
