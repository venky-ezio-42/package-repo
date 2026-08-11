class VersionSelector:

    @staticmethod
    def belongs_to_major(
        version: str,
        version_type: str,
        major: str,
    ) -> bool:

        match version_type:

            case "SEMVER":
                return version.startswith(f"{major}.")

            case "SEMVER_SUFFIX":
                return version.startswith(f"{major}.")
            
            case "SEMVER_LETTER":
                return version.startswith(f"{major}.")

            case "INTEGER":
                return version == str(major)

            case "YEAR_DATE":
                return version.startswith(str(major))

            case "YEAR_ALPHA":
                return version.startswith(str(major))

            case _:
                return False

    @staticmethod
    def latest(
        versions: list[str],
    ) -> str:

        return sorted(versions)[-1]