import pandas as pd

from src.transform.tables.order_item import transform_order_items

def test_transform_order_items():

    df = pd.DataFrame({
        "order_id": ["1", "2"],
        "order_item_id": [1, 2],
        "product_id": ["A", "B"],
        "seller_id": ["S1", "S2"],
        "shipping_limit_date": ["2023-01-01", "2023-01-01"],
        "price": [100, -10],
        "freight_value": [20, 5],
    })

    result = transform_order_items(df)

    assert len(result) == 1
    assert result.iloc[0]["price"] == 100