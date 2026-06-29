import logging
import pandas as pd

from transform.helper import validate_columns, validate_required_values

"""
seller_id* string
seller_zip_code_prefix* string
seller_city* string
seller_state* string

sem duplicatas
"""

TABLE_NAME = "sellers"

SELLER_ID = "seller_id"
SELLER_ZIP_CODE_PREFIX = "seller_zip_code_prefix"
SELLER_CITY = "seller_city"
SELLER_STATE = "seller_state"

COLUMNS = [
    SELLER_ID,
    SELLER_ZIP_CODE_PREFIX,
    SELLER_CITY,
    SELLER_STATE,
]

REQUIRED_COLUMNS = [
    SELLER_ID,
    SELLER_ZIP_CODE_PREFIX,
    SELLER_CITY,
    SELLER_STATE,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_sellers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_sellers(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            PRODUCT_ID,
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_sellers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[SELLER_ID] = (
        df[SELLER_ID]
        .astype("string")
        .str.strip()
    )

    df[SELLER_ZIP_CODE_PREFIX] = (
        df[SELLER_ZIP_CODE_PREFIX]
        .astype("string")
        .str.replace(r"\D", "", regex=True)
    )

    df[SELLER_CITY] = (
        df[SELLER_CITY]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    df[SELLER_STATE] = (
        df[SELLER_STATE]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    return df