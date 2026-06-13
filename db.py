import sqlite3
from config import DB_PATH


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alerts_sent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                condition TEXT NOT NULL,
                trigger_price REAL NOT NULL,
                actual_price REAL NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def insert_price(symbol: str, price: float):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO prices (symbol, price) VALUES (?, ?)",
            (symbol, price),
        )


def record_alert(symbol: str, condition: str, trigger_price: float, actual_price: float):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO alerts_sent (symbol, condition, trigger_price, actual_price) VALUES (?, ?, ?, ?)",
            (symbol, condition, trigger_price, actual_price),
        )


def already_alerted_today(symbol: str, condition: str, trigger_price: float) -> bool:
    """Prevent duplicate alerts for the same condition within the same calendar day."""
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT 1 FROM alerts_sent
            WHERE symbol = ?
              AND condition = ?
              AND trigger_price = ?
              AND date(sent_at) = date('now')
            LIMIT 1
            """,
            (symbol, condition, trigger_price),
        ).fetchone()
    return row is not None
