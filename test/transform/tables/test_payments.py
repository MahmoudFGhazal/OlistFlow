import pandas as pd

from src.transform.tables.payment import transform_payments

def test_transform_payments():

    df = pd.DataFrame({
        "order_id": ["1", "2"],
        "payment_sequential": [1, 0],
        "payment_type": ["credit_card", "pix"],
        "payment_installments": [3, 2],
    })

    result = transform_payments(df)

    assert len(result) == 1
    assert result.iloc[0]["payment_type"] == "credit_card"