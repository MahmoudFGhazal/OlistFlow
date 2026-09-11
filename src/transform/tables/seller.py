import logging
import pandas as pd

from src.errors.decorator import capture_error
from src.transform.tables.comum import normalize_city

from ..helper import validate_columns, validate_required_values

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
SELLER_NORMALIZE_CITY = "seller_normalize_city"

INPUT_COLUMNS = [
    SELLER_ID,
    SELLER_ZIP_CODE_PREFIX,
    SELLER_CITY,
    SELLER_STATE,
]

COLUMNS = [
    *INPUT_COLUMNS,
    SELLER_NORMALIZE_CITY,
]

REQUIRED_COLUMNS = [
    SELLER_ID,
    SELLER_ZIP_CODE_PREFIX,
    SELLER_CITY,
    SELLER_STATE,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

@capture_error(
    stage="TRANSFORM",
    table="sellers"
)
def transform_sellers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(df, required_columns=INPUT_COLUMNS, table_name=TABLE_NAME)

    df = _clean_sellers(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            SELLER_ID,
        ]
    )

    df = _apply_sellers_rules(df)

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
        .str.replace(r"\s+", " ", regex=True)
        .str.split("/", n=1)
        .str[0]
        .str.strip()
        .str.lower()
    )

    df[SELLER_STATE] = (
        df[SELLER_STATE]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    return df

def _apply_sellers_rules(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Aplicando regras {TABLE_NAME}")

    df = df.copy()

    # =========================
    # Regra 1: estado deve ter exatamente 2 caracteres (UF)
    # =========================
    df = df[df[SELLER_STATE].str.len() == 2]

    # =========================
    # Regra 2: cidade não pode ser string vazia após limpeza
    # =========================
    df = df[df[SELLER_CITY] != ""]

    # =========================
    # Regra 3: CEP deve ter pelo menos 5 dígitos
    # =========================
    df = df[df[SELLER_ZIP_CODE_PREFIX].str.len() >= 5]

    # =========================
    # Regra 3: Remover acentos da cidade
    # =========================
    df[SELLER_NORMALIZE_CITY] = df[SELLER_CITY].apply(normalize_city)
    
    return df