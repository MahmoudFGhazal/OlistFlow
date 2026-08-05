import logging
from pathlib import Path
import pandas as pd

from src.errors.decorator import capture_error
from src.errors.exceptions import ExtractionError

DATASET_PATH = Path("data/raw")

logger = logging.getLogger("etl.extract")

DATASET_NAMES = {
    "olist_customers_dataset": "customers",
    "olist_geolocation_dataset": "locations",
    "olist_orders_dataset": "orders",
    "olist_order_items_dataset": "order_items",
    "olist_order_payments_dataset": "payments",
    "olist_order_reviews_dataset": "reviews",
    "olist_products_dataset": "products",
    "olist_sellers_dataset": "sellers",
    "product_category_name_translation": "categories",
}

def read_file(file: Path):
    try:
        if file.suffix == ".csv" or file.suffix == ".xlsx":
            if file.suffix == ".csv":
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            logger.info(
                f"Arquivo {file.name} carregado "
                f"({len(df)} linhas)"
            )

            return df
    except Exception as error:
        raise ExtractionError(
            f"Erro ao processar o arquivo {file.name}"
        ) from error
    
    logger.warning(
        f"Arquivo ignorado: {file.name} "
        f"(tipo {file.suffix} não suportado)"
    )

    return None

@capture_error("extract")
def extract_dataset(path: Path = DATASET_PATH):
    logger.info("Iniciando a extração de arquivos")

    datasets = {}

    for file in path.iterdir():
        if file.is_file():
            data = read_file(file)

            if data is not None:
                dataset_name = DATASET_NAMES.get(
                    file.stem,
                    file.stem
                )

                datasets[dataset_name] = data


    return datasets
    