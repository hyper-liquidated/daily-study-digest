#!/usr/bin/env python3
import sqlite3
import os

# Find the project root folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Path where the database file will live
db_path = os.path.join(BASE_DIR, "studies.db")

# The instructions (schema) for creating our table
schema = """
CREATE TABLE IF NOT EXISTS studies (
    id INTEGER PRIMARY KEY,
    track TEXT,
    title TEXT,
    authors TEXT,
    source TEXT,
    summary TEXT,
    why_notable TEXT,
    doi TEXT,
    source_url TEXT,
    year INTEGER,
    used_in_digest BOOLEAN DEFAULT FALSE,
    extra TEXT
);
"""

def init_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Run the instructions above
    cur.executescript(schema)

    # Save changes and close the file
    conn.commit()
    conn.close()
    print(f"Database created or updated at: {db_path}")

if __name__ == "__main__":
    init_db()
