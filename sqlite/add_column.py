import sqlite3

conn = sqlite3.connect("package_registry_v2.db")
cur = conn.cursor()

# --------------------------------------------------
# Add version_regex column
# --------------------------------------------------

try:

    cur.execute("""
        ALTER TABLE packages
        ADD COLUMN version_regex TEXT;
    """)

    print("Added version_regex column.")

except sqlite3.OperationalError:

    print("version_regex already exists.")

# --------------------------------------------------
# Default: Semantic Version
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d+\\.\\d+(?:\\.\\d+)?)';
""")

# --------------------------------------------------
# YYYYMMDD
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(20\\d{4})'
    WHERE package_name = 'iana-etc';
""")

# --------------------------------------------------
# YYYY<letter>
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(20\\d{2}[a-z])'
    WHERE package_name = 'tzdata';
""")

# --------------------------------------------------
# SQLite Autoconf (3510200)
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d{7})'
    WHERE package_name = 'sqlite';
""")

# --------------------------------------------------
# SQLite Documentation (3510200)
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d{7})'
    WHERE package_name = 'sqlite-doc';
""")

# --------------------------------------------------
# LFS Bootscripts (20250827)
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(20\\d{4})'
    WHERE package_name = 'lfs-bootscripts';
""")

# --------------------------------------------------
# Udev LFS (20230818)
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(20\\d{4})'
    WHERE package_name = 'udev-lfs';
""")

# --------------------------------------------------
# Systemd Man Pages (259.1)
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d+\\.\\d+)'
    WHERE package_name = 'systemd-man-pages';
""")

# --------------------------------------------------
# Tcl Source
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d+\\.\\d+\\.\\d+)'
    WHERE package_name = 'tcl-src';
""")

# --------------------------------------------------
# Tcl HTML
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d+\\.\\d+\\.\\d+)'
    WHERE package_name = 'tcl-html';
""")

# --------------------------------------------------
# Python HTML Docs
# --------------------------------------------------

cur.execute("""
    UPDATE packages
    SET version_regex = '(\\d+\\.\\d+\\.\\d+)'
    WHERE package_name = 'python-docs';
""")

conn.commit()

print("Done.")

conn.close()