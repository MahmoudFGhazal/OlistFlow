import logging
import pandas as pd

logger = logging.getLogger("etl.transform.sellers")


def transform_sellers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando sellers")

    df = df.drop_duplicates(subset=["seller_id"])

    logger.info(f"Sellers transformada ({len(df)} registros)")
    return df