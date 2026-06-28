import logging
from typing import TypedDict

import pandas as pd

from .helper import normalize_nulls
from .customer import transform_customers
from .location import transform_locations
from .orders import transform_order_items, transform_orders, transform_payments, transform_reviews
from .product import transform_products
from .seller import transform_sellers
from .categories import transform_categories

logger = logging.getLogger("etl.transform")

class TransformedDatasets(TypedDict):
    categories: pd.DataFrame
    customers: pd.DataFrame
    locations: pd.DataFrame
    sellers: pd.DataFrame
    products: pd.DataFrame
    orders: pd.DataFrame
    order_items: pd.DataFrame
    payments: pd.DataFrame
    reviews: pd.DataFrame

def transform_datasets(raw: dict[str, pd.DataFrame]) -> TransformedDatasets:
    logger.info("Inciando Transformações")

    raw = {
        name: normalize_nulls(df)
        for name, df in raw.items()
    }

    categories = transform_categories(raw["categories"])
    customers = transform_customers(raw["customers"])
    locations = transform_locations(raw["locations"])
    sellers = transform_sellers(raw["sellers"])
    products = transform_products(raw["products"], categories)
    orders = transform_orders(raw["orders"])
    order_items = transform_order_items(raw["order_items"])
    payments = transform_payments(raw["payments"])
    reviews = transform_reviews(raw["reviews"])

    logger.info("Transformação concluídas")

    return TransformedDatasets(
        categories=categories,
        customers=customers,
        locations=locations,
        sellers=sellers,
        products=products,
        orders=orders,
        order_items=order_items,
        payments=payments,
        reviews=reviews,
    )