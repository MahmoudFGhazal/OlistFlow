import logging
import pandas as pd

from src.errors.decorator import capture_error

from ..enums import UF
from ..helper import validate_columns, validate_required_values

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

@capture_error(
    stage="TRANSFORM",
    table="locations"
)
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

    df = _apply_locations_rules(df)

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

def _apply_locations_rules(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Aplicando regras {TABLE_NAME}")

    df = df.copy()

    # =========================
    # Regra 1: ZIP CODE = 5 caracteres
    # =========================
    df = df[df[GEOLOCATION_ZIP_CODE_PREFIX].str.len() == 5]

    # =========================
    # Regra 2: STATE válido (Brasil)
    # =========================
    df = df[df[GEOLOCATION_STATE].isin([u.value for u in UF])]

    # =========================
    # Regra 3: LATITUDE válida
    # =========================
    df = df[
        df[GEOLOCATION_LAT].between(-90, 90)
    ]

    # =========================
    # Regra 4: LONGITUDE válida
    # =========================
    df = df[
        df[GEOLOCATION_LNG].between(-180, 180)
    ]

    # =========================
    # Regra 5: Normalização geográfica por ZIP + STATE + CITY
    # (média de lat/lng por localidade)
    # =========================
    GROUP_COLS = [
        GEOLOCATION_ZIP_CODE_PREFIX,
        GEOLOCATION_STATE,
        GEOLOCATION_CITY,
    ]

    df[GEOLOCATION_LAT] = df.groupby(GROUP_COLS)[GEOLOCATION_LAT].transform("mean")
    df[GEOLOCATION_LNG] = df.groupby(GROUP_COLS)[GEOLOCATION_LNG].transform("mean")

    return df