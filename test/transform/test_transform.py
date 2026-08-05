import pandas as pd

from src.transform import transform_datasets

def test_transform_datasets(raw_dataset):

    result = transform_datasets(raw_dataset)

    expected = {
        "categories",
        "customers",
        "locations",
        "sellers",
        "products",
        "orders",
        "order_items",
        "payments",
        "reviews",
    }

    assert set(result.keys()) == expected

    for table in expected:
        assert isinstance(result[table], pd.DataFrame)
        assert len(result[table]) == 2