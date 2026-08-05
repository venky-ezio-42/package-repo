import sqlite3

conn = sqlite3.connect("package_registry.db")
cur = conn.cursor()

cur.executescript("""
UPDATE packages
SET fetcher = 'GitHubFetcher'
WHERE download_url LIKE 'https://github.com/%';

UPDATE packages
SET fetcher = 'PyPIFetcher'
WHERE download_url LIKE 'https://pypi.org/%'
   OR download_url LIKE 'https://files.pythonhosted.org/%';

UPDATE packages
SET fetcher = 'SourceForgeFetcher'
WHERE download_url LIKE '%sourceforge.net/%'
   OR download_url LIKE '%downloads.sourceforge.net/%'
   OR download_url LIKE '%prdownloads.sourceforge.net/%';

UPDATE packages
SET fetcher = 'GenericFetcher'
WHERE download_url LIKE '%cpan.metacpan.org/%'
   OR download_url LIKE '%www.cpan.org/%';

UPDATE packages
SET fetcher = 'IndexFetcher'
WHERE fetcher IS NULL
   OR fetcher = '';
""")

conn.commit()

print("Fetchers updated successfully.")

conn.close()