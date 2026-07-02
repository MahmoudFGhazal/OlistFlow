import logging
import pandas as pd

from ..enums import PaymentType
from ..helper import validate_columns, validate_required_values

"""
order_id* string
payment_sequencial* integer
payment_type* string
payment_installments* integer
"""

TABLE_NAME="payments"

ORDER_ID = "order_id"
PAYMENT_SEQUENTIAL = "payment_sequential"
PAYMENT_TYPE = "payment_type"
PAYMENT_INSTALLMENTS = "payment_installments"

COLUMNS = [
    ORDER_ID,
    PAYMENT_SEQUENTIAL,
    PAYMENT_TYPE,
    PAYMENT_INSTALLMENTS,
]

REQUIRED_COLUMNS = [
    ORDER_ID,
    PAYMENT_SEQUENTIAL,
    PAYMENT_TYPE,
    PAYMENT_INSTALLMENTS,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_payments(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(
        df,
        required_columns=COLUMNS,
        table_name=TABLE_NAME
    )

    df = _clean_payments(df)

    df = validate_required_values(
        df,
        required_columns=REQUIRED_COLUMNS,
        table_name=TABLE_NAME
    )

    df = _apply_payments_rules(df)
    
    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[ORDER_ID] = (
        df[ORDER_ID]
        .astype("string")
        .str.strip()
    )

    df[PAYMENT_SEQUENTIAL] = pd.to_numeric(
        df[PAYMENT_SEQUENTIAL],
        errors="coerce"
    ).astype("Int64")

    df[PAYMENT_TYPE] = (
        df[PAYMENT_TYPE]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df[PAYMENT_INSTALLMENTS] = pd.to_numeric(
        df[PAYMENT_INSTALLMENTS],
        errors="coerce"
    ).astype("Int64")

    return df

def _apply_payments_rules(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Aplicando regras {TABLE_NAME}")

    df = df.copy()

    # =========================
    # Regra 1: payment_sequential válido (>= 1)
    # =========================
    df = df[df[PAYMENT_SEQUENTIAL] >= 1]

    # =========================
    # Regra 2: payment_type deve estar no enum
    # =========================
    df = df[df[PAYMENT_TYPE].isin([u.value for u in PaymentType])]

    # =========================
    # Regra 3: installments deve ser >= 1
    # =========================
    df = df[df[PAYMENT_INSTALLMENTS] >= 1]

    return df