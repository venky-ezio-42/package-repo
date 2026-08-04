import sqlite3

conn = sqlite3.connect("package_registry.db")
cur = conn.cursor()

# Add new columns (run only once)
try:
    cur.execute("ALTER TABLE packages ADD COLUMN parser TEXT DEFAULT 'auto'")
except sqlite3.OperationalError:
    pass

try:
    cur.execute("ALTER TABLE packages ADD COLUMN checksum_url TEXT")
except sqlite3.OperationalError:
    pass

try:
    cur.execute("ALTER TABLE packages ADD COLUMN signature_url TEXT")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()