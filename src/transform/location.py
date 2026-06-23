import logging
import pandas as pd

logger = logging.getLogger("etl.transform.locations")


def transform_locations(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformando locations")

    # Dataset tem ~260k linhas duplicadas por CEP
    # Agrupa por CEP e cidade/estado, tirando a mediana das coordenadas
    df = (
        df.groupby(
            ["geolocation_zip_code_prefix", "geolocation_city", "geolocation_state"],
            as_index=False,
        )
        .agg(
            geolocation_lat=("geolocation_lat", "median"),
            geolocation_lng=("geolocation_lng", "median"),
        )
    )

    logger.info(f"Locations transformada ({len(df)} registros únicos por CEP)")
    return df