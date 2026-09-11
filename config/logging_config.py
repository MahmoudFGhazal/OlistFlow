from datetime import datetime
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

DEBUG = False

def setup_logging():
    log_level = logging.DEBUG if DEBUG else logging.INFO

    etl_handler = logging.FileHandler(
        LOG_DIR / f"etl_{run_id}.log",
        mode="a",
        encoding="utf-8"
    )
    etl_handler.setLevel(log_level)

    error_handler = logging.FileHandler(
        LOG_DIR / "errors.log",
        mode="w",
        encoding="utf-8"
    )
    error_handler.setLevel(logging.WARNING)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s - "
            "%(levelname)s - "
            "[%(name)s] - "
            "%(message)s"
        ),
        handlers=[etl_handler, error_handler, stream_handler]
    )

    logging.captureWarnings(True)