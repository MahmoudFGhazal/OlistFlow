import pandas as pd

from src.transform.tables.seller import transform_sellers


def test_transform_sellers():

    df = pd.DataFrame({
        "seller_id": ["1", "2"],
        "seller_zip_code_prefix": ["12345", "12"],
        "seller_city": [" São Paulo ", ""],
        "seller_state": ["sp", "SP"],
    })

    result = transform_sellers(df)

    assert len(result) == 1

    row = result.iloc[0]

    assert row["seller_city"] == "são paulo"
    assert row["seller_state"] == "SP"