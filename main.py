import logging 
from src.extract.excel_reader import extract_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Iniciando ETL")

datasets = extract_dataset()

logging.info("Arquivos carregados")