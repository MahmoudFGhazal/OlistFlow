import pandas as pd

from src.transform.tables.location import transform_locations

def test_transform_locations():

    df = pd.DataFrame({
        "geolocation_zip_code_prefix": ["12345", "12345"],
        "geolocation_lat": [-23.5, -23.7],
        "geolocation_lng": [-46.5, -46.7],
        "geolocation_city": [" São Paulo ", "São Paulo"],
        "geolocation_state": ["sp", "SP"],
    })

    result = transform_locations(df)

    assert len(result) == 2

    assert result.iloc[0]["geolocation_city"] == "são paulo"
    assert result.iloc[0]["geolocation_state"] == "SP"