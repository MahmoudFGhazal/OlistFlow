import logging
import pandas as pd

from .helper import validate_columns, validate_required_values

"""
product_category_name* string
product_category_name_english string

sem duplicatas
"""

TABLE_NAME="categories"

PRODUCT_CATEGORY_NAME = "product_category_name"
PRODUCT_CATEGORY_NAME_ENGLISH = "product_category_name_english"

COLUMNS = [
    PRODUCT_CATEGORY_NAME,
    PRODUCT_CATEGORY_NAME_ENGLISH
]

REQUIRED_COLUMNS = [
    PRODUCT_CATEGORY_NAME,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_categories(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando categorias")
 
    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_categories(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            PRODUCT_CATEGORY_NAME        
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")
    return df

def _clean_categories(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[PRODUCT_CATEGORY_NAME] = (
        df[PRODUCT_CATEGORY_NAME]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    df[PRODUCT_CATEGORY_NAME_ENGLISH] = (
        df[PRODUCT_CATEGORY_NAME_ENGLISH]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    return df