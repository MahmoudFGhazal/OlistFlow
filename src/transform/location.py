import logging
import pandas as pd

from transform.helper import validate_columns, validate_required_values

"""
geolocation_zip_code_prefix* string
geolocation_lat* float
geolocation_lng* float
geolocation_city* string
geolocation_state* string

sem duplicatas
"""

TABLE_NAME="locations"

GEOLOCATION_ZIP_CODE_PREFIX = "geolocation_zip_code_prefix"
GEOLOCATION_LAT = "geolocation_lat"
GEOLOCATION_LNG = "geolocation_lng"
GEOLOCATION_CITY = "geolocation_city"
GEOLOCATION_STATE = "geolocation_state"

COLUMNS = [
    GEOLOCATION_ZIP_CODE_PREFIX,
    GEOLOCATION_LAT,
    GEOLOCATION_LNG,
    GEOLOCATION_CITY,
    GEOLOCATION_STATE,
]

REQUIRED_COLUMNS = [
    GEOLOCATION_ZIP_CODE_PREFIX,
    GEOLOCATION_LAT,
    GEOLOCATION_LNG,
    GEOLOCATION_CITY,
    GEOLOCATION_STATE,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_locations(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(df, required_columns=COLUMNS, table_name=TABLE_NAME)

    df = _clean_locations(df)

    df = validate_required_values(df, required_columns=REQUIRED_COLUMNS, table_name=TABLE_NAME)

    df = df.drop_duplicates(
        subset=[
            GEOLOCATION_ZIP_CODE_PREFIX,
            GEOLOCATION_LAT,
            GEOLOCATION_LNG
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df

def _clean_locations(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    df[GEOLOCATION_ZIP_CODE_PREFIX] = (
        df[GEOLOCATION_ZIP_CODE_PREFIX]
        .astype("string")
        .str.replace(r"\D", "", regex=True)
    )

    df[GEOLOCATION_LAT] = pd.to_numeric(
        df[GEOLOCATION_LAT],
        errors="coerce"
    )

    df[GEOLOCATION_LNG] = pd.to_numeric(
        df[GEOLOCATION_LNG],
        errors="coerce"
    )

    df[GEOLOCATION_CITY] = (
        df[GEOLOCATION_CITY]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    df[GEOLOCATION_STATE] = (
        df[GEOLOCATION_STATE]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.upper()
    )

    return df