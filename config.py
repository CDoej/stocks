import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

EMAIL_SENDER = os.environ["STOCKS_EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["STOCKS_EMAIL_PASSWORD"]
EMAIL_RECIPIENT = os.environ["STOCKS_EMAIL_RECIPIENT"]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

DB_PATH = str(Path(__file__).parent / "stocks.db")
WATCHLIST_PATH = str(Path(__file__).parent / "watchlist.json")
