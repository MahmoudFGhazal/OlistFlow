import logging
import pandas as pd

logger = logging.getLogger("etl.transform.orders")

DATE_COLS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando orders")

    df = df.drop_duplicates(subset=["order_id"])

    for col in DATE_COLS:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    cancelled_mask = df["order_status"].isin(["canceled", "unavailable"])
    n_cancelled = cancelled_mask.sum()
    if n_cancelled:
        logger.info(f"{n_cancelled} pedidos cancelados/unavailable (datas de entrega NaT é esperado)")

    logger.info(f"Orders transformada ({len(df)} registros)")
    return df


def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando order_items")

    df = df.drop_duplicates(subset=["order_id", "order_item_id"])

    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")

    logger.info(f"Order_items transformada ({len(df)} registros)")
    return df


def transform_payments(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando payments")

    df = df.drop_duplicates(subset=["order_id", "payment_sequential"])

    logger.info(f"Payments transformada ({len(df)} registros)")
    return df


def transform_reviews(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando reviews")

    df = df.drop_duplicates(subset=["review_id"])

    df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], errors="coerce")
    df["review_answer_timestamp"] = pd.to_datetime(df["review_answer_timestamp"], errors="coerce")

    df["review_comment_title"] = df["review_comment_title"].fillna("")
    df["review_comment_message"] = df["review_comment_message"].fillna("")

    logger.info(f"Reviews transformada ({len(df)} registros)")
    return df