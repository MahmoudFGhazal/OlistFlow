import logging
import pandas as pd

from src.errors.decorator import capture_error
from src.transform.tables.comum import normalize_city

from ..enums import UF
from ..helper import validate_columns, validate_required_values

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
CUSTOMER_NORMALIZE_CITY = "customer_normalize_city"
CUSTOMER_STATE = "customer_state"

INPUT_COLUMNS = [
    CUSTOMER_ID,
    CUSTOMER_UNIQUE_ID,
    CUSTOMER_ZIP_CODE_PREFIX,
    CUSTOMER_CITY,
    CUSTOMER_STATE,
]

COLUMNS = [
    *INPUT_COLUMNS,
    CUSTOMER_NORMALIZE_CITY,
]

REQUIRED_COLUMNS = [
    CUSTOMER_ID,
    CUSTOMER_UNIQUE_ID,
    CUSTOMER_ZIP_CODE_PREFIX,
    CUSTOMER_CITY,
    CUSTOMER_STATE
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

@capture_error(
    stage="TRANSFORM",
    table="customers"
)
def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando customers")

    validate_columns(df, required_columns=INPUT_COLUMNS, table_name=TABLE_NAME)

    df = _clean_customers(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            CUSTOMER_ID
        ]
    )

    df = _apply_customers_rules(df)

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[CUSTOMER_ID] = (
        df[CUSTOMER_ID]
        .astype("string")
        .str.strip()
    )

    df[CUSTOMER_UNIQUE_ID] = (
        df[CUSTOMER_UNIQUE_ID]
        .astype("string")
        .str.strip()
    )

    df[CUSTOMER_ZIP_CODE_PREFIX] = (
        df[CUSTOMER_ZIP_CODE_PREFIX]
        .astype("string")
        .str.replace(r"\D", "", regex=True)
    )

    df[CUSTOMER_CITY] = (
        df[CUSTOMER_CITY]
        .astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.split("/", n=1)
        .str[0]
        .str.strip()
        .str.lower()
    )

    df[CUSTOMER_STATE] = (
        df[CUSTOMER_STATE]
        .astype("string")
        .str.replace(" ", "", regex=True)
        .str.upper()
    )

    return df

def _apply_customers_rules(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Aplicando regras {TABLE_NAME}")

    df = df.copy()

    # =========================
    # Regra 1: ZIP CODE = 5 caracteres
    # =========================
    df = df[df[CUSTOMER_ZIP_CODE_PREFIX].str.len() == 5]

    # =========================
    # Regra 2: STATE deve estar no ENUM (UF Brasil)
    # =========================
    df = df[df[CUSTOMER_STATE].isin([u.value for u in UF])]

    # =========================
    # Regra 3: Remover acentos da cidade
    # =========================
    df[CUSTOMER_NORMALIZE_CITY] = df[CUSTOMER_CITY].apply(normalize_city)

    return df