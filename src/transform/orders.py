import logging
import pandas as pd

from transform.helper import validate_columns, validate_required_values

"""
order_id* string
customer_id* string
order_status* string
order_purchase_timestamp* datetime
order_approved_at* datetime
order_delivered_carrier_date* datetime
order_delivered_customer_date* datetime
order_estimated_delivery_date* datetime


sem duplicatas
"""

TABLE_NAME="orders"

ORDER_ID = "order_id"
CUSTOMER_ID = "customer_id"
ORDER_STATUS = "order_status"
ORDER_PURCHASE_TIMESTAMP = "order_purchase_timestamp"
ORDER_APPROVED_AT = "order_approved_at"
ORDER_DELIVERED_CARRIER_DATE = "order_delivered_carrier_date"
ORDER_DELIVERED_CUSTOMER_DATE = "order_delivered_customer_date"
ORDER_ESTIMATED_DELIVERY_DATE = "order_estimated_delivery_date"

COLUMNS = [
    ORDER_ID,
    CUSTOMER_ID,
    ORDER_STATUS,
    ORDER_PURCHASE_TIMESTAMP,
    ORDER_APPROVED_AT,
    ORDER_DELIVERED_CARRIER_DATE,
    ORDER_DELIVERED_CUSTOMER_DATE,
    ORDER_ESTIMATED_DELIVERY_DATE,
]

REQUIRED_COLUMNS = [
    ORDER_ID,
    CUSTOMER_ID,
    ORDER_STATUS,
    ORDER_PURCHASE_TIMESTAMP,
    ORDER_APPROVED_AT,
    ORDER_DELIVERED_CARRIER_DATE,
    ORDER_DELIVERED_CUSTOMER_DATE,
    ORDER_ESTIMATED_DELIVERY_DATE,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_orders(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            ORDER_ID,
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[ORDER_ID] = (
        df[ORDER_ID]
        .astype("string")
        .str.replace(" ", "", regex=True)
    )

    df[CUSTOMER_ID] = (
        df[CUSTOMER_ID]
        .astype("string")
        .str.replace(" ", "", regex=True)
    )

    df[ORDER_STATUS] = (
        df[ORDER_STATUS]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    df[ORDER_ID] = (
        df[ORDER_ID]
        .astype("string")
        .str.replace(" ", "", regex=True)
    )

    df[ORDER_PURCHASE_TIMESTAMP] = pd.to_datetime(
        df[ORDER_PURCHASE_TIMESTAMP],
        errors="coerce"
    )