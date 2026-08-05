import pytest
import pandas as pd


@pytest.fixture
def raw_dataset():
    return {

        "categories": pd.DataFrame({
            "product_category_name": [
                "beauty",
                "furniture"
            ],
            "product_category_name_english": [
                "beauty",
                "furniture"
            ]
        }),

        "customers": pd.DataFrame({
            "customer_id": [
                "cust_1",
                "cust_2"
            ],
            "customer_unique_id": [
                "unique_1",
                "unique_2"
            ],
            "customer_zip_code_prefix": [
                "12345",
                "54321"
            ],
            "customer_city": [
                "São Paulo",
                "Rio de Janeiro"
            ],
            "customer_state": [
                "SP",
                "RJ"
            ]
        }),

        "locations": pd.DataFrame({
            "geolocation_zip_code_prefix": [
                "12345",
                "54321"
            ],
            "geolocation_lat": [
                -23.5505,
                -22.9068
            ],
            "geolocation_lng": [
                -46.6333,
                -43.1729
            ],
            "geolocation_city": [
                "São Paulo",
                "Rio de Janeiro"
            ],
            "geolocation_state": [
                "SP",
                "RJ"
            ]
        }),

        "sellers": pd.DataFrame({
            "seller_id": [
                "seller_1",
                "seller_2"
            ],
            "seller_zip_code_prefix": [
                "12345",
                "54321"
            ],
            "seller_city": [
                "São Paulo",
                "Rio de Janeiro"
            ],
            "seller_state": [
                "SP",
                "RJ"
            ]
        }),

        "products": pd.DataFrame({
            "product_id": [
                "prod_1",
                "prod_2"
            ],
            "product_category_name": [
                "beauty",
                "furniture"
            ],
            "product_photos_qty": [
                3,
                2
            ],
            "product_weight_g": [
                500,
                1200
            ],
            "product_length_cm": [
                20,
                50
            ],
            "product_height_cm": [
                10,
                40
            ],
            "product_width_cm": [
                15,
                30
            ]
        }),

        "orders": pd.DataFrame({
            "order_id": [
                "order_1",
                "order_2"
            ],
            "customer_id": [
                "cust_1",
                "cust_2"
            ],
            "order_status": [
                "delivered",
                "delivered"
            ],
            "order_purchase_timestamp": [
                "2023-01-01 10:00:00",
                "2023-02-01 09:00:00"
            ],
            "order_approved_at": [
                "2023-01-01 10:10:00",
                "2023-02-01 09:10:00"
            ],
            "order_delivered_carrier_date": [
                "2023-01-02",
                "2023-02-02"
            ],
            "order_delivered_customer_date": [
                "2023-01-05",
                "2023-02-05"
            ],
            "order_estimated_delivery_date": [
                "2023-01-06",
                "2023-02-06"
            ]
        }),

        "order_items": pd.DataFrame({
            "order_id": [
                "order_1",
                "order_2"
            ],
            "order_item_id": [
                1,
                2
            ],
            "product_id": [
                "prod_1",
                "prod_2"
            ],
            "seller_id": [
                "seller_1",
                "seller_2"
            ],
            "shipping_limit_date": [
                "2023-01-02",
                "2023-02-02"
            ],
            "price": [
                120.50,
                300.00
            ],
            "freight_value": [
                20,
                35
            ]
        }),

        "payments": pd.DataFrame({
            "order_id": [
                "order_1",
                "order_2"
            ],
            "payment_sequential": [
                1,
                1
            ],
            "payment_type": [
                "credit_card",
                "debit_card"
            ],
            "payment_installments": [
                2,
                1
            ]
        }),

        "reviews": pd.DataFrame({
            "review_id": [
                "review_1",
                "review_2"
            ],
            "order_id": [
                "order_1",
                "order_2"
            ],
            "review_score": [
                5,
                4
            ],
            "review_comment_title": [
                "Excelente",
                "Bom"
            ],
            "review_comment_message": [
                "Produto ótimo",
                "Gostei"
            ],
            "review_creation_date": [
                "2023-01-06",
                "2023-02-06"
            ],
            "review_answer_timestamp": [
                "2023-01-07",
                "2023-02-07"
            ]
        })
    }