import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

EMAIL_SENDER = os.environ["STOCKS_EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["STOCKS_EMAIL_PASSWORD"]
EMAIL_RECIPIENT = os.environ["STOCKS_EMAIL_RECIPIENT"]
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
SUPABASE_EMAIL = os.environ.get("SUPABASE_EMAIL", "")
SUPABASE_PASSWORD = os.environ.get("SUPABASE_PASSWORD", "")

DB_PATH = str(ROOT_DIR / "stocks.db")
WATCHLIST_PATH = str(ROOT_DIR / "watchlist.json")
