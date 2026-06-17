import datetime
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

handler = logging.FileHandler(
    f"logs/etl_{run_id}.log",
    encoding="utf-8"
)

DEBUG = False

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "[%(name)s] - "
        "%(message)s"
    ),
    handlers=[
        handler,
        logging.StreamHandler()
    ]
)

logging.captureWarnings(True)