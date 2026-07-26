import json
import pytest
import tempfile
import os
from src.fetcher import check_condition, load_watchlist


class TestCheckCondition:
    def test_above_triggered(self):
        assert check_condition(250.0, "above", 220.0) is True

    def test_above_at_exact_price(self):
        assert check_condition(220.0, "above", 220.0) is True

    def test_above_not_triggered(self):
        assert check_condition(210.0, "above", 220.0) is False

    def test_below_triggered(self):
        assert check_condition(140.0, "below", 150.0) is True

    def test_below_at_exact_price(self):
        assert check_condition(150.0, "below", 150.0) is True

    def test_below_not_triggered(self):
        assert check_condition(160.0, "below", 150.0) is False

    def test_unknown_condition_raises(self):
        with pytest.raises(ValueError, match="Unknown condition"):
            check_condition(100.0, "sideways", 100.0)


class TestLoadWatchlist:
    def test_loads_valid_watchlist(self, tmp_path, monkeypatch):
        watchlist = [{"symbol": "AAPL", "condition": "below", "price": 270.0}]
        path = tmp_path / "watchlist.json"
        path.write_text(json.dumps(watchlist))
        monkeypatch.setattr("src.fetcher.WATCHLIST_PATH", str(path))

        result = load_watchlist()

        assert len(result) == 1
        assert result[0]["symbol"] == "AAPL"

    def test_empty_watchlist(self, tmp_path, monkeypatch):
        path = tmp_path / "watchlist.json"
        path.write_text("[]")
        monkeypatch.setattr("src.fetcher.WATCHLIST_PATH", str(path))

        result = load_watchlist()

        assert result == []
