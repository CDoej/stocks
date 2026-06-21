import sqlite3
from contextlib import contextmanager
from src.config import DB_PATH


@contextmanager
def get_conn():
    with sqlite3.connect(DB_PATH) as conn:
        yield conn


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


def insert_price(conn: sqlite3.Connection, symbol: str, price: float):
    conn.execute(
        "INSERT INTO prices (symbol, price) VALUES (?, ?)",
        (symbol, price),
    )


def record_alert(conn: sqlite3.Connection, symbol: str, condition: str, trigger_price: float, actual_price: float):
    conn.execute(
        "INSERT INTO alerts_sent (symbol, condition, trigger_price, actual_price) VALUES (?, ?, ?, ?)",
        (symbol, condition, trigger_price, actual_price),
    )


def already_alerted_today(conn: sqlite3.Connection, symbol: str, condition: str, trigger_price: float) -> bool:
    """Return True if an alert for this exact condition was already sent today (local time)."""
    row = conn.execute(
        """
        SELECT 1 FROM alerts_sent
        WHERE symbol = ?
          AND condition = ?
          AND trigger_price = ?
          -- sent_at is stored as UTC; convert both sides to localtime so the
          -- day boundary matches the user's calendar, not midnight UTC.
          AND date(sent_at, 'localtime') = date('now', 'localtime')
        LIMIT 1
        """,
        (symbol, condition, trigger_price),
    ).fetchone()
    return row is not None
