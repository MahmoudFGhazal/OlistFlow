import logging
import pandas as pd

logger = logging.getLogger("etl.transform.products")


def transform_products(df: pd.DataFrame, categories: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando products")

    df = df.drop_duplicates(subset=["product_id"])

    df = df.merge(
        categories[["category_name_pt", "category_name_en"]],
        left_on="product_category_name",
        right_on="category_name_pt",
        how="left",
    )
    df = df.drop(columns=["product_category_name", "category_name_pt"])
    df = df.rename(columns={"category_name_en": "product_category_name"})

    dimension_cols = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for col in dimension_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median)

    logger.info(f"Products transformada ({len(df)} registros)")
    return df