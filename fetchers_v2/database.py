import sqlite3


class Database:

    def __init__(self, database_path):
        self.database_path = database_path

    def connect(self):
        return sqlite3.connect(
            self.database_path
        )

    def get_packages(self):

        connection = self.connect()

        connection.row_factory = sqlite3.Row

        try:

            cursor = connection.execute(
                """
                SELECT
                    package_id,
                    package_name,
                    package_prefix,
                    source_url,
                    version_type
                FROM packages
                ORDER BY package_name
                """
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    def get_versions(self, package_id):

        connection = self.connect()

        connection.row_factory = sqlite3.Row

        try:

            cursor = connection.execute(
                """
                SELECT
                    id,
                    package_id,
                    version,
                    major,
                    minor,
                    patch,
                    suffix,
                    fetched,
                    fetched_at,
                    latest
                FROM versions
                WHERE package_id = ?
                ORDER BY version
                """,
                (package_id,)
            )

            return [
                dict(row)
                for row in cursor.fetchall()
            ]

        finally:

            connection.close()

    def get_package_with_versions(
        self,
        package_id,
    ):

        connection = self.connect()

        connection.row_factory = sqlite3.Row

        try:

            package_cursor = connection.execute(
                """
                SELECT
                    id,
                    package_name,
                    package_prefix,
                    source_url,
                    version_type
                FROM packages
                WHERE id = ?
                """,
                (package_id,)
            )

            package = package_cursor.fetchone()

            if package is None:
                return None

            version_cursor = connection.execute(
                """
                SELECT
                    id,
                    package_id,
                    version,
                    major,
                    minor,
                    patch,
                    suffix,
                    fetched,
                    fetched_at,
                    latest
                FROM versions
                WHERE package_id = ?
                ORDER BY version
                """,
                (package_id,)
            )

            result = dict(package)

            result["versions"] = [
                dict(row)
                for row in version_cursor.fetchall()
            ]

            return result

        finally:

            connection.close()
