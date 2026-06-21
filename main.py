import logging
import warnings
from pathlib import Path
warnings.filterwarnings("ignore", message=".*LibreSSL.*")

from src.fetcher import run

LOG_PATH = Path(__file__).parent / "fetch.log"

handlers = [logging.StreamHandler()]
if not __import__("os").environ.get("GITHUB_ACTIONS"):
    handlers.append(logging.FileHandler(LOG_PATH))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=handlers,
)

if __name__ == "__main__":
    run()
