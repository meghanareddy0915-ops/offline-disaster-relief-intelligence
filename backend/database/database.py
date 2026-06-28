import sqlite3

DATABASE_NAME = "disaster_relief.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disaster_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disaster_type TEXT,
        location TEXT,
        people_affected INTEGER,
        resources_required TEXT,
        priority TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()