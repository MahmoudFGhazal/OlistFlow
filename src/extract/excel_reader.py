import logging
from pathlib import Path
import pandas as pd

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

def _read_file(file: Path):
    try:
        if file.suffix == ".csv":
            df = pd.read_csv(file)

            logger.info(
                f"Arquivo {file.name} carregado "
                f"({len(df)} linhas)"
            )

            return df
    except Exception:
        logger.exception(
            f"Erro ao processar o arquivo {file.name}"
        )
        raise
    
    logger.warning(
        f"Arquivo ignorado: {file.name} "
        f"(tipo {file.suffix} não suportado)"
    )

    return None

def extract_dataset(path: Path = DATASET_PATH):
    logger.info("Iniciando a extração de arquivos")

    datasets = {}

    for file in path.iterdir():
        if file.is_file():
            data = _read_file(file)

            if data is not None:
                dataset_name = DATASET_NAMES.get(
                    file.stem,
                    file.stem
                )

                datasets[dataset_name] = data


    return datasets
    