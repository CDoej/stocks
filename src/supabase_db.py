import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_EMAIL, SUPABASE_PASSWORD

CET = ZoneInfo("Europe/Copenhagen")

logger = logging.getLogger(__name__)

_client: Optional[Client] = None


def get_client() -> Client:
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set.")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        if SUPABASE_EMAIL and SUPABASE_PASSWORD:
            _client.auth.sign_in_with_password({"email": SUPABASE_EMAIL, "password": SUPABASE_PASSWORD})
            logger.info("Signed in to Supabase as %s", SUPABASE_EMAIL)
    return _client


def insert_price(symbol: str, price: float):
    get_client().table("prices").insert({
        "symbol": symbol,
        "price": price,
    }).execute()


def record_alert(symbol: str, condition: str, trigger_price: float, actual_price: float):
    get_client().table("alerts_sent").insert({
        "symbol": symbol,
        "condition": condition,
        "trigger_price": trigger_price,
        "actual_price": actual_price,
    }).execute()


def already_alerted_today(symbol: str, condition: str, trigger_price: float) -> bool:
    midnight_cet = datetime.now(CET).replace(hour=0, minute=0, second=0, microsecond=0)
    result = (
        get_client()
        .table("alerts_sent")
        .select("id")
        .eq("symbol", symbol)
        .eq("condition", condition)
        .eq("trigger_price", trigger_price)
        .gte("sent_at", midnight_cet.isoformat())
        .limit(1)
        .execute()
    )
    return len(result.data) > 0
