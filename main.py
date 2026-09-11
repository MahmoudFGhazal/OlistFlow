import os
import time

from dotenv import load_dotenv
import logging

from sqlalchemy import create_engine 
from config.logging_config import setup_logging
from src.errors.decorator import capture_error
from src.load import load_data
from src.load.loaders.sql.postgre.postgre_loader import PostgreLoader
from src.transform import transform_datasets
from src.extract import extract_dataset

load_dotenv()

database_url = os.getenv("API_DATABASE_URL")

engine = create_engine(database_url)

logger = logging.getLogger("etl")

@capture_error("main")
def main():
    setup_logging()

    start = time.perf_counter()

    logger.info("Iniciando ETL")

    datasets = extract_dataset()

    logger.info(
        f"Arquivos carregados em "
        f"{time.perf_counter() - start:.2f}s"
    )

    start = time.perf_counter()

    transformed = transform_datasets(datasets)

    logger.info(f"Transformações concluídas em {time.perf_counter() - start:.2f}s")

    load_data(transformed, PostgreLoader(engine))

    logger.info("Carga de dados concluida com sucesso!")

if __name__ == "__main__":
    main()