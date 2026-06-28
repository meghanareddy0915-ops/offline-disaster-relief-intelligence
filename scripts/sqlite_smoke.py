import sqlite3
def main():
    with sqlite3.connect(":memory:") as conn:
        conn.execute(
            """
            CREATE TABLE disaster_requests (
                id TEXT PRIMARY KEY,
                urgency TEXT NOT NULL,
                people_affected INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO disaster_requests (id, urgency, people_affected) VALUES (?, ?, ?)",
            ("smoke", "critical", 52),
        )
        row = conn.execute(
            "SELECT urgency, people_affected FROM disaster_requests WHERE id = ?",
            ("smoke",),
        ).fetchone()

    if row != ("critical", 52):
        raise SystemExit("SQLite smoke check failed")

    print("sqlite smoke passed")


if __name__ == "__main__":
    main()
