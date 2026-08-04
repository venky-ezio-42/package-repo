import sqlite3

def get_packages():

    conn = sqlite3.connect("sqlite/package_registry.db")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM packages
        WHERE enabled = 1
    """)

    packages = [dict(row) for row in cur.fetchall()]

    conn.close()

    return packages