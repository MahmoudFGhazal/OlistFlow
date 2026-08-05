import pandas as pd

from src.transform.tables.customer import transform_customers


def test_transform_customers():

    df = pd.DataFrame({
        "customer_id": ["1", "1", "2"],
        "customer_unique_id": ["10", "10", "20"],
        "customer_zip_code_prefix": ["12345", "12345", "12"],
        "customer_city": [" São Paulo ", " São Paulo ", "Rio"],
        "customer_state": ["sp", "sp", "XX"],
    })

    result = transform_customers(df)

    assert len(result) == 1

    row = result.iloc[0]

    assert row["customer_city"] == "são paulo"
    assert row["customer_state"] == "SP"
    assert row["customer_zip_code_prefix"] == "12345"