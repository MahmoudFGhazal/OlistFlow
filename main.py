import time
from config import *
import logging 
from src.transform import transform_datasets
from src.extract import extract_dataset

logger = logging.getLogger("etl")

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