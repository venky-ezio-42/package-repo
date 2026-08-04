import sqlite3

conn = sqlite3.connect("package_registry.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT * FROM packages")

for package in cursor.fetchall():
    print(package["package_name"])
    print(package["host"])
    print(package["repo_family"])
    print(package["fetcher"])
    print(package["listing_url"])
    print(package["download_url"])
    print()


"""
CREATE TABLE packages (
    id INTEGER PRIMARY KEY,
    package_name TEXT,
    repo_family TEXT,
    fetcher TEXT,
    host TEXT,
    listing_url TEXT,
    download_url TEXT,
    current_version TEXT,
    latest_version TEXT,
    enabled INTEGER,
    status TEXT
);
"""