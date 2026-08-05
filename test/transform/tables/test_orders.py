import pandas as pd

from src.transform.tables.orders import transform_orders

def test_transform_orders():

    df = pd.DataFrame({
        "order_id": ["1"],
        "customer_id": ["10"],
        "order_status": [" Delivered "],
        "order_purchase_timestamp": ["2023-01-01"],
        "order_approved_at": ["2023-01-02"],
        "order_delivered_carrier_date": ["2023-01-03"],
        "order_delivered_customer_date": ["2023-01-05"],
        "order_estimated_delivery_date": ["2023-01-10"],
    })

    result = transform_orders(df)

    assert len(result) == 1
    assert result.iloc[0]["order_status"] == "delivered"