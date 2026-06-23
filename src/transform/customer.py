import logging
import pandas as pd

logger = logging.getLogger("etl.transform.customers")


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando customers")

    df = df.drop_duplicates(subset=["customer_id"])

    logger.info(f"Customers transformada ({len(df)} registros)")
    return df