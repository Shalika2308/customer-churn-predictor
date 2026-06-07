import sqlite3
import json
import os


def create_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(
        "database/predictions.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_data TEXT,
            prediction TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


def save_prediction(
    input_data,
    prediction,
    confidence
):

    conn = sqlite3.connect("database/predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            input_data,
            prediction,
            confidence
        )
        VALUES (?, ?, ?)
    """,
    (
        json.dumps(input_data),
        prediction,
        confidence
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()