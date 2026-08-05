from datetime import datetime
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

def setup_logging():
    handler = [
        logging.FileHandler(
            LOG_DIR / "etl.log"
        ),
        logging.FileHandler(
            LOG_DIR / "errors.log"
        )
    ]

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
            *handler,
            logging.StreamHandler()
        ]
    )

    logging.captureWarnings(True)