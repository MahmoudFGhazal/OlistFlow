
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
    

#Limpar
def validate_columns(df: pd.DataFrame, required_columns: list[str], table_name: str) -> None:
    missing = set(required_columns) - set(df.columns)

    if missing:
        logger.error(f"{table_name} - Possui as seguintes colunas ausentes: {sorted(missing)}")
        raise ValueError(
            f"{table_name} - Possui as seguintes colunas ausentes: {sorted(missing)}"
        )

def validate_required_values(df: pd.DataFrame, required_columns: list[str], table_name: str) -> pd.DataFrame:
    nulls = df[required_columns].isna().sum()

    invalid = nulls[nulls > 0]

    if not invalid.empty:
        logger.info(f"{table_name} - Colunas com valores nulos:\n{invalid}")
        logger.info(f"{table_name} - Total de valores nulos encontrados: {invalid.sum()}")

    return df.dropna(subset=required_columns)