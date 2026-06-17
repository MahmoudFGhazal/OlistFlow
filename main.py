import time
from config import *
import logging 
from src.extract import extract_dataset

logger = logging.getLogger("etl")

start = time.perf_counter()

logger.info("Iniciando ETL")

datasets = extract_dataset()

elapsed = time.perf_counter() - start

logger.info(
    f"Arquivos carregados em {elapsed:.2f}s"
)
