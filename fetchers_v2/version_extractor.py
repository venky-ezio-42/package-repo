import re

from .directory_creator import DirectoryCreator


class VersionExtractor:

    EXTENSION_REGEX = re.compile(
        r"\.(?:"
        r"tar\.gz|"
        r"tar\.xz|"
        r"tar\.bz2|"
        r"tgz|"
        r"zip"
        r")"
        r"(?:"
        r"\.(?:asc|sig|sha256|md5)(?:\.txt)?"
        r")?$"
    )

    VERSION_PATTERNS = {

        "SEMVER": re.compile(
            r"(?P<version>\d+\.\d+(?:\.\d+)?)$"
        ),

        "INTEGER": re.compile(
            r"(?P<version>\d+)$"
        ),

        "YEAR_DATE": re.compile(
            r"(?P<version>20\d{2})\d{4}"
        ),

        "YEAR_ALPHA": re.compile(
            r"(?P<version>20\d{2}[a-z])$"
        ),

        "SEMVER_SUFFIX": re.compile(
            r"(?P<version>\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)*)$"
        ),

        "SEMVER_LETTER": re.compile(
            r"(?P<version>\d+\.\d+\.\d+[a-z])$"
        ),
    }

    @classmethod
    def extract_version(
        cls,
        filename,
        version_type,
        package_prefix=None,
    ):

        #
        # Remove archive extension
        #
        filename = cls.EXTENSION_REGEX.sub(
            "",
            filename,
        )

        #
        # Remove package prefix when supplied
        #
        if package_prefix:

            hyphen_prefix = f"{package_prefix}-"

            if filename.startswith(hyphen_prefix):

                # package-version
                filename = filename[
                    len(hyphen_prefix):
                ]

            elif filename.startswith(package_prefix):

                # packageversion
                filename = filename[
                    len(package_prefix):
                ]

            else:

                raise ValueError(
                    f"'{filename}' does not belong to "
                    f"package '{package_prefix}'"
                )

        #
        # SourceForge/GitHub style version directories
        # may begin with 'v'
        #
        filename = filename.removeprefix("v")

        #
        # Look up version pattern
        #
        try:

            pattern = cls.VERSION_PATTERNS[
                version_type
            ]

        except KeyError:

            raise ValueError(
                f"Unknown version type '{version_type}'"
            )

        #
        # Extract version
        #
        match = pattern.search(
            filename
        )

        if not match:

            raise ValueError(
                f"Unable to extract "
                f"{version_type} version "
                f"from '{filename}'"
            )

        return match.group("version")

    @classmethod
    def create_version_directory(
        cls,
        package_name,
        version,
        version_type,
        base_path="packages",
    ):

        package_directory = DirectoryCreator.create(
            base_path,
            package_name,
        )

        match version_type:

            #
            # 1
            # 1.2
            # 1.2.3
            #
            case "SEMVER":

                parts = version.split(".")

                major_directory = DirectoryCreator.create(
                    package_directory,
                    f"{package_name}-{parts[0]}",
                )

                if len(parts) == 1:
                    return major_directory

                minor_directory = DirectoryCreator.create(
                    major_directory,
                    f"{package_name}-{parts[0]}.{parts[1]}",
                )

                if len(parts) == 2:
                    return minor_directory

                return DirectoryCreator.create(
                    minor_directory,
                    f"{package_name}-{version}",
                )

            #
            # 1.2.3-alpha
            # 1.2.3-beta
            #
            case "SEMVER_SUFFIX":

                numeric = version.split(
                    "-",
                    1
                )[0]

                parts = numeric.split(".")

                major_directory = DirectoryCreator.create(
                    package_directory,
                    f"{package_name}-{parts[0]}",
                )

                minor_directory = DirectoryCreator.create(
                    major_directory,
                    f"{package_name}-{parts[0]}.{parts[1]}",
                )

                return DirectoryCreator.create(
                    minor_directory,
                    f"{package_name}-{version}",
                )

            #
            # 1.2.3a
            # 1.2.3j
            #
            case "SEMVER_LETTER":

                numeric = re.match(
                    r"\d+\.\d+\.\d+",
                    version,
                ).group()

                parts = numeric.split(".")

                major_directory = DirectoryCreator.create(
                    package_directory,
                    f"{package_name}-{parts[0]}",
                )

                minor_directory = DirectoryCreator.create(
                    major_directory,
                    f"{package_name}-{parts[0]}.{parts[1]}",
                )

                return DirectoryCreator.create(
                    minor_directory,
                    f"{package_name}-{version}",
                )

            #
            # 20250827
            #
            case "YEAR_DATE":

                year_directory = DirectoryCreator.create(
                    package_directory,
                    version[:4],
                )

                return DirectoryCreator.create(
                    year_directory,
                    f"{package_name}-{version}",
                )

            #
            # 2025c
            #
            case "YEAR_ALPHA":

                year_directory = DirectoryCreator.create(
                    package_directory,
                    version[:4],
                )

                return DirectoryCreator.create(
                    year_directory,
                    f"{package_name}-{version}",
                )

            #
            # 28
            # 247
            #
            case "INTEGER":

                return DirectoryCreator.create(
                    package_directory,
                    f"{package_name}-{version}",
                )

            #
            # Unknown
            #
            case _:

                raise ValueError(
                    f"Unknown version type "
                    f"'{version_type}'"
                )