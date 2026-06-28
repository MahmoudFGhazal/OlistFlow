
import logging

import pandas as pd

logger = logging.getLogger("etl.transform.helper")

#Tratar
def normalize_nulls(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace(
        [
            "",
            " ",
            "NULL",
            "null",
            "NaN",
            "nan",
            "N/A",
        ],
        pd.NA,
    )
    
