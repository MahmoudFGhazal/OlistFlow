import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

Path("logs").mkdir(exist_ok=True)

handler = RotatingFileHandler(
    "logs/etl.log",
    maxBytes=5_000_000,
    backupCount=3,
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