import logging
import pandas as pd


logger = logging.getLogger("etl.transform.categories")

def transform_categories(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando categorias")
 
    df = df.drop_duplicates(subset=["product_category_name"])
    df = df.rename(columns={
        "product_category_name": "category_name_pt",
        "product_category_name_english": "category_name_en",
    })
    df = df.dropna(subset=["category_name_pt"])
 
    logger.info(f"Categories transformada ({len(df)} registros)")
    return df
