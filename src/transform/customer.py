import logging
import pandas as pd

from .helper import validate_columns, validate_required_values

"""
customer_id* string
customer_unique_id* string
customer_zip_code_prefix*: string 5 caracteres
customer_city*: string minusculo
customer_state*: string maisculo

sem duplicatas
"""

TABLE_NAME="customers"

CUSTOMER_ID = "customer_id"
CUSTOMER_UNIQUE_ID = "customer_unique_id"
CUSTOMER_ZIP_CODE_PREFIX = "customer_zip_code_prefix"
CUSTOMER_CITY = "customer_city"
CUSTOMER_STATE = "customer_state"

COLUMNS = [
    CUSTOMER_ID,
    CUSTOMER_UNIQUE_ID,
    CUSTOMER_ZIP_CODE_PREFIX,
    CUSTOMER_CITY,
    CUSTOMER_STATE,
]

REQUIRED_COLUMNS = [
    CUSTOMER_ID,
    CUSTOMER_UNIQUE_ID,
    CUSTOMER_ZIP_CODE_PREFIX,
    CUSTOMER_CITY,
    CUSTOMER_STATE
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando customers")

    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_customers(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            CUSTOMER_ID
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[CUSTOMER_ID] = (
        df[CUSTOMER_ID]
        .astype("string")
        .str.replace(" ", "", regex=True)
    )

    df[CUSTOMER_UNIQUE_ID] = (
        df[CUSTOMER_UNIQUE_ID]
        .astype("string")
        .str.replace(" ", "", regex=True)
    )

    df[CUSTOMER_ZIP_CODE_PREFIX] = (
        df[CUSTOMER_ZIP_CODE_PREFIX]
        .astype("string")
        .str.replace(r"\D", "", regex=True)
    )

    df[CUSTOMER_CITY] = (
        df[CUSTOMER_CITY]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    df[CUSTOMER_STATE] = (
        df[CUSTOMER_STATE]
        .astype("string")
        .str.replace(" ", "", regex=True)
        .str.upper()
    )

    return df