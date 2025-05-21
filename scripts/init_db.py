#!/usr/bin/env python3
import os
import psycopg2

# Read the DATABASE_URL from the environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Please set the DATABASE_URL environment variable")

# Connect to Postgres
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Schema: create table if it doesn't exist
schema = """
CREATE TABLE IF NOT EXISTS studies (
    id SERIAL PRIMARY KEY,
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
    cur.execute(schema)
    conn.commit()
    print("Initialized Postgres database with studies table.")

if __name__ == "__main__":
    init_db()
    cur.close()
    conn.close()
