

from typing import TypedDict

import pandas as pd


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