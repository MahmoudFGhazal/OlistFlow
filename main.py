import time
from config import *
import logging 
from src.errors.decorator import capture_error
from src.transform import transform_datasets
from src.extract import extract_dataset

logger = logging.getLogger("etl")

@capture_error("main")
def main():
    setup_logging()

    start = time.perf_counter()

    logger.info("Iniciando ETL")

    datasets = extract_dataset()

    elapsed = time.perf_counter() - start

    logger.info(
        f"Arquivos carregados em {elapsed:.2f}s"
    )

    start = time.perf_counter()

    transformed = transform_datasets(datasets)

    logger.info(f"Transformações concluídas em {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    main()