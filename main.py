import logging
import warnings
from pathlib import Path
warnings.filterwarnings("ignore", message=".*LibreSSL.*")

from src.fetcher import run

LOG_PATH = Path(__file__).parent / "fetch.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(),
    ],
)

if __name__ == "__main__":
    run()
