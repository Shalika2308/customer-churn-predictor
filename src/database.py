import sqlite3


def create_database():

    conn = sqlite3.connect("database/predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenure_months INTEGER,
            monthly_charges REAL,
            contract TEXT,
            prediction TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


def save_prediction(
    tenure_months,
    monthly_charges,
    contract,
    prediction,
    confidence
):


    conn = sqlite3.connect("database/predictions.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            tenure_months,
            monthly_charges,
            contract,
            prediction,
            confidence
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        tenure_months,
        monthly_charges,
        contract,
        prediction,
        confidence
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()