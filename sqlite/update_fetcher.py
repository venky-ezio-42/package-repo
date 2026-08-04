import sqlite3

conn = sqlite3.connect("package_registry.db")
cur = conn.cursor()

cur.execute("""
UPDATE packages
SET fetcher = 'IndexFetcher'
WHERE download_url NOT LIKE '%github.com%'
  AND download_url NOT LIKE '%pypi.org%'
  AND download_url NOT LIKE '%pythonhosted.org%'
  AND download_url NOT LIKE '%sourceforge.net%'
  AND download_url NOT LIKE '%cpan%'
""")

print(f"Updated {cur.rowcount} rows.")

conn.commit()
conn.close()