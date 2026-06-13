#!/usr/bin/env python3
"""
Fetch stock prices, store them in the database, and send email alerts
when a watched stock crosses its configured threshold.

Run directly or via cron:
    python3 /Users/christiandoej/Projects/stocks/fetch.py
"""

import json
import sys
import yfinance as yf

from config import WATCHLIST_PATH
from db import init_db, insert_price, record_alert, already_alerted_today
from alert import send_alert


def load_watchlist():
    with open(WATCHLIST_PATH) as f:
        return json.load(f)


def check_condition(actual: float, condition: str, target: float) -> bool:
    if condition == "above":
        return actual >= target
    if condition == "below":
        return actual <= target
    raise ValueError(f"Unknown condition: {condition!r}. Use 'above' or 'below'.")


def main():
    init_db()
    watchlist = load_watchlist()

    if not watchlist:
        print("Watchlist is empty.")
        return

    symbols = [entry["symbol"] for entry in watchlist]
    print(f"Fetching prices for: {', '.join(symbols)}")

    tickers = yf.Tickers(" ".join(symbols))

    for entry in watchlist:
        symbol = entry["symbol"]
        condition = entry["condition"]
        target_price = float(entry["price"])

        try:
            info = tickers.tickers[symbol].fast_info
            current_price = info.last_price
            if current_price is None:
                print(f"  {symbol}: no price data available, skipping.")
                continue
        except Exception as exc:
            print(f"  {symbol}: failed to fetch price — {exc}")
            continue

        name = entry.get("name", symbol)
        currency = entry.get("currency", "USD")

        insert_price(symbol, current_price)
        print(f"  {name} ({symbol}): {currency} {current_price:.2f} (target {condition} {currency} {target_price:.2f})")

        if check_condition(current_price, condition, target_price):
            if already_alerted_today(symbol, condition, target_price):
                print(f"    → Condition met but alert already sent today, skipping.")
            else:
                send_alert(name, symbol, currency, condition, target_price, current_price)
                record_alert(symbol, condition, target_price, current_price)


if __name__ == "__main__":
    sys.exit(main())
