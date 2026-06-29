import logging
import pandas as pd

from transform.helper import validate_columns, validate_required_values

"""
product_id* string
product_category_name* string
product_photos_qty* integer
product_weight_g* integer
product_length_cm* number
product_height_cm* number
product_width_cm* number

sem duplicatas
"""

TABLE_NAME="products"

PRODUCT_ID = "product_id"
PRODUCT_CATEGORY_NAME = "product_category_name"
PRODUCT_PHOTOS_QTY = "product_photos_qty"
PRODUCT_WEIGHT_G = "product_weight_g"
PRODUCT_LENGTH_CM = "product_length_cm"
PRODUCT_HEIGHT_CM = "product_height_cm"
PRODUCT_WIDTH_CM = "product_width_cm"

COLUMNS = [
    PRODUCT_ID,
    PRODUCT_CATEGORY_NAME,
    PRODUCT_PHOTOS_QTY,
    PRODUCT_WEIGHT_G,
    PRODUCT_LENGTH_CM,
    PRODUCT_HEIGHT_CM,
    PRODUCT_WIDTH_CM,
]

REQUIRED_COLUMNS = [
    PRODUCT_ID,
    PRODUCT_CATEGORY_NAME,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_products(df: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_products(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            PRODUCT_ID,
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_products(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[PRODUCT_ID] = (
        df[PRODUCT_ID]
        .astype("string")
        .str.strip()
    )

    df[PRODUCT_CATEGORY_NAME] = (
        df[PRODUCT_CATEGORY_NAME]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    df[PRODUCT_PHOTOS_QTY] = pd.to_numeric(
        df[PRODUCT_PHOTOS_QTY],
        errors="coerce"
    ).astype("Int64")

    df[PRODUCT_WEIGHT_G] = pd.to_numeric(
        df[PRODUCT_WEIGHT_G],
        errors="coerce"
    ).astype("Int64")

    df[PRODUCT_LENGTH_CM] = pd.to_numeric(
        df[PRODUCT_LENGTH_CM],
        errors="coerce"
    )

    df[PRODUCT_HEIGHT_CM] = pd.to_numeric(
        df[PRODUCT_HEIGHT_CM],
        errors="coerce"
    )

    df[PRODUCT_WIDTH_CM] = pd.to_numeric(
        df[PRODUCT_WIDTH_CM],
        errors="coerce"
    )

    return df