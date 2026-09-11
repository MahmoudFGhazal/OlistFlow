import logging

import pandas as pd

from src.errors.decorator import capture_error
from src.transform.types import TransformedDatasets

from .tables.review import transform_reviews
from .tables.payment import transform_payments
from .tables.order_item import transform_order_items
from .helper import normalize_nulls
from .tables.customer import transform_customers
from .tables.geolocations import transform_geolocations
from .tables.orders import transform_orders
from .tables.product import transform_products
from .tables.seller import transform_sellers
from .tables.category import transform_categories

logger = logging.getLogger("etl.transform")

@capture_error("transform")
def transform_datasets(raw: dict[str, pd.DataFrame]) -> TransformedDatasets:
    logger.info("Inciando Transformações")

    raw = {
        name: normalize_nulls(df)
        for name, df in raw.items()
    }

    categories = transform_categories(raw["categories"])
    customers = transform_customers(raw["customers"])
    geolocations = transform_geolocations(raw["locations"])
    sellers = transform_sellers(raw["sellers"])
    products = transform_products(raw["products"])
    orders = transform_orders(raw["orders"])
    order_items = transform_order_items(raw["order_items"])
    payments = transform_payments(raw["payments"])
    reviews = transform_reviews(raw["reviews"])

    logger.info("Transformação concluídas")

    return TransformedDatasets(
        categories=categories,
        customers=customers,
        geolocations=geolocations,
        sellers=sellers,
        products=products,
        orders=orders,
        order_items=order_items,
        payments=payments,
        reviews=reviews,
    )