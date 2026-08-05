import pandas as pd

from src.transform.tables.category import transform_categories

def test_transform_categories():

    df = pd.DataFrame({
        "product_category_name": [
            " Beleza ",
            " beleza "
        ],
        "product_category_name_english": [
            " Beauty ",
            " beauty "
        ]
    })

    result = transform_categories(df)

    assert len(result) == 1
    assert result.iloc[0]["product_category_name"] == "beleza"
    assert result.iloc[0]["product_category_name_english"] == "beauty"