import logging
import pandas as pd

from ..helper import validate_columns, validate_required_values

"""
order_id* string
order_item_id* string
product_id* string
seller_id* string
shipping_limit_date* datetime
price* float
freight_value* float
"""

TABLE_NAME="order_items"

ORDER_ID = "order_id"
ORDER_ITEM_ID = "order_item_id"
PRODUCT_ID = "product_id"
SELLER_ID = "seller_id"
SHIPPING_LIMIT_DATE = "shipping_limit_date"
PRICE = "price"
FREIGHT_VALUE = "freight_value"

COLUMNS = [
    ORDER_ID,
    ORDER_ITEM_ID,
    PRODUCT_ID,
    SELLER_ID,
    SHIPPING_LIMIT_DATE,
    PRICE,
    FREIGHT_VALUE,
]

REQUIRED_COLUMNS = [
    ORDER_ID,
    ORDER_ITEM_ID,
    PRODUCT_ID,
    SELLER_ID,
    SHIPPING_LIMIT_DATE,
    PRICE,
    FREIGHT_VALUE,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_order_items(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    string_columns = [
        ORDER_ID,
        PRODUCT_ID,
        SELLER_ID,
    ]

    for column in string_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    df[ORDER_ITEM_ID] = pd.to_numeric(
        df[ORDER_ITEM_ID],
        errors="coerce"
    ).astype("Int64")

    df[SHIPPING_LIMIT_DATE] = pd.to_datetime(
        df[SHIPPING_LIMIT_DATE],
        errors="coerce"
    )

    df[PRICE] = pd.to_numeric(
        df[PRICE],
        errors="coerce"
    )

    df[FREIGHT_VALUE] = pd.to_numeric(
        df[FREIGHT_VALUE],
        errors="coerce"
    )

    return df