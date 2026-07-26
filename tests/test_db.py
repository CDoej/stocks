import pytest
import sqlite3
import src.db as db_module
from src.db import init_db, insert_price, record_alert, already_alerted_today, get_conn


@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr(db_module, "DB_PATH", db_path)
    init_db()
    yield


class TestInsertPrice:
    def test_insert_and_retrieve(self):
        with get_conn() as conn:
            insert_price(conn, "AAPL", 291.13)
            row = conn.execute("SELECT symbol, price FROM prices").fetchone()
        assert row == ("AAPL", 291.13)

    def test_multiple_inserts(self):
        with get_conn() as conn:
            insert_price(conn, "AAPL", 291.13)
            insert_price(conn, "AAPL", 295.00)
            count = conn.execute("SELECT COUNT(*) FROM prices").fetchone()[0]
        assert count == 2


class TestAlreadyAlertedToday:
    def test_no_alert_sent(self):
        with get_conn() as conn:
            assert already_alerted_today(conn, "AAPL", "below", 270.0) is False

    def test_alert_sent_today(self):
        with get_conn() as conn:
            record_alert(conn, "AAPL", "below", 270.0, 265.0)
            assert already_alerted_today(conn, "AAPL", "below", 270.0) is True

    def test_different_symbol_not_matched(self):
        with get_conn() as conn:
            record_alert(conn, "AAPL", "below", 270.0, 265.0)
            assert already_alerted_today(conn, "MSFT", "below", 270.0) is False

    def test_different_condition_not_matched(self):
        with get_conn() as conn:
            record_alert(conn, "AAPL", "below", 270.0, 265.0)
            assert already_alerted_today(conn, "AAPL", "above", 270.0) is False

    def test_different_price_not_matched(self):
        with get_conn() as conn:
            record_alert(conn, "AAPL", "below", 270.0, 265.0)
            assert already_alerted_today(conn, "AAPL", "below", 300.0) is False
