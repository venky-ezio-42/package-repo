
class PackageService:

    def __init__(self, database):
        self.database = database

    def get_packages(self):

        packages = self.database.get_packages()

        for package in packages:

            versions = self.database.get_versions(
                package["package_id"]
            )

            package["versions"] = versions

            if versions:

                # Prefer latest version marked in DB
                latest = next(
                    (
                        version
                        for version in versions
                        if version["latest"]
                    ),
                    None,
                )

                if latest is None:
                    latest = versions[-1]

                package["major_version"] = (
                    latest["major"]
                )

            else:

                package["major_version"] = None

        return packages

    def get_package(self, package_id):

        package = (
            self.database
            .get_package_with_versions(package_id)
        )

        if package is None:
            return None

        versions = package["versions"]

        if versions:

            latest = next(
                (
                    version
                    for version in versions
                    if version["latest"]
                ),
                None,
            )

            if latest is None:
                latest = versions[-1]

            package["major_version"] = (
                latest["major"]
            )

        else:

            package["major_version"] = None

        return package
