import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

EMAIL_SENDER = os.environ["STOCKS_EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["STOCKS_EMAIL_PASSWORD"]
EMAIL_RECIPIENT = os.environ["STOCKS_EMAIL_RECIPIENT"]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

DB_PATH = str(ROOT_DIR / "stocks.db")
WATCHLIST_PATH = str(ROOT_DIR / "watchlist.json")
