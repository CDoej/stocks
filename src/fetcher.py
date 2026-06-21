import json
import logging
import yfinance as yf

from src.config import WATCHLIST_PATH, SUPABASE_URL
from src.alert import send_alert

logger = logging.getLogger(__name__)


def _get_store():
    if SUPABASE_URL:
        logger.info("Using Supabase for storage.")
        import src.supabase_db as store
    else:
        logger.info("Using local SQLite for storage.")
        import src.db as store
        store.init_db()
    return store


def load_watchlist():
    with open(WATCHLIST_PATH) as f:
        return json.load(f)


def check_condition(actual: float, condition: str, target: float) -> bool:
    if condition == "above":
        return actual >= target
    if condition == "below":
        return actual <= target
    raise ValueError(f"Unknown condition: {condition!r}. Use 'above' or 'below'.")


def run():
    store = _get_store()
    watchlist = load_watchlist()

    if not watchlist:
        logger.warning("Watchlist is empty.")
        return

    symbols = [entry["symbol"] for entry in watchlist]
    logger.info(f"Fetching prices for: {', '.join(symbols)}")

    tickers = yf.Tickers(" ".join(symbols))

    for entry in watchlist:
        symbol = entry["symbol"]
        name = entry.get("name", symbol)
        currency = entry.get("currency", "USD")
        condition = entry["condition"]
        target_price = float(entry["price"])

        try:
            info = tickers.tickers[symbol].fast_info
            current_price = info.last_price
            if current_price is None:
                logger.warning(f"{name} ({symbol}): no price data available, skipping.")
                continue
        except Exception as exc:
            logger.error(f"{name} ({symbol}): failed to fetch price — {exc}")
            continue

        store.insert_price(symbol, current_price)
        logger.info(f"{name} ({symbol}): {currency} {current_price:.2f} (target {condition} {currency} {target_price:.2f})")

        if check_condition(current_price, condition, target_price):
            if store.already_alerted_today(symbol, condition, target_price):
                logger.info(f"{name} ({symbol}): condition met but alert already sent today, skipping.")
            else:
                send_alert(name, symbol, currency, condition, target_price, current_price)
                store.record_alert(symbol, condition, target_price, current_price)
