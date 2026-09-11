



import logging

import pandas as pd

from src.errors.decorator import capture_error
from src.load.loaders.prepare_data import PrepareData
from src.load.loaders.sql.table_models import TABLE_MODELS, build_table_requirements
from src.transform.tables import orders
from src.transform.tables import orders
from src.transform.types import TransformedDatasets

logger = logging.getLogger("etl.load.prepare")

@capture_error("prepare", table="cities") 
def _prepare_cities(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando cidades para carga")

    geolocations = datasets["geolocations"]
    customers = datasets["customers"]
    sellers = datasets["sellers"]
    
    states_map = loaded["states"].set_index("sta_uf")["sta_id"]

    cities = pd.concat(
        [
            geolocations[["geolocation_city", "geolocation_normalize_city", "geolocation_state"]].rename(
                columns={
                    "geolocation_city": "cit_name",
                    "geolocation_normalize_city": "cit_normalize_name",
                    "geolocation_state": "cit_sta_uf",
                }
            ),
            customers[["customer_city", "customer_normalize_city", "customer_state"]].rename(
                columns={
                    "customer_city": "cit_name",
                    "customer_normalize_city": "cit_normalize_name",
                    "customer_state": "cit_sta_uf",
                }
            ),
            sellers[["seller_city", "seller_normalize_city", "seller_state"]].rename(
                columns={
                    "seller_city": "cit_name",
                    "seller_normalize_city": "cit_normalize_name",
                    "seller_state": "cit_sta_uf",
                }
            ),
        ],
        ignore_index=True
    ).drop_duplicates(["cit_normalize_name", "cit_sta_uf"])

    cities["cit_sta_id"] = cities["cit_sta_uf"].map(states_map)

    missing = cities[cities["cit_sta_id"].isna()]
    if not missing.empty:
        logger.warning(
            f"{len(missing)} cidades com UF não encontrada em core.states: "
            f"{sorted(missing['cit_sta_uf'].unique())}"
        )
        cities = cities.dropna(subset=["cit_sta_id"])

    cities["cit_sta_id"] = cities["cit_sta_id"].astype(int)
    cities = cities.drop(columns=["cit_sta_uf"])

    logger.info(f"Cidades preparados para carga ({len(cities)} registros)")

    return cities

@capture_error("prepare", table="locations")
def _prepare_locations(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando locations para carga")

    geolocations = datasets["geolocations"]
    customers = datasets["customers"]
    sellers = datasets["sellers"]

    cities = loaded["cities"]
    states = loaded["states"]

    locations = pd.concat(
            [
                geolocations[["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng", "geolocation_normalize_city", "geolocation_state"]].rename(
                    columns={
                        "geolocation_zip_code_prefix": "loc_code_prefix",
                        "geolocation_lat": "loc_lat",
                        "geolocation_lng": "loc_lng",
                        "geolocation_normalize_city": "city",
                        "geolocation_state": "uf",
                    }
                ),
                customers[["customer_zip_code_prefix", "customer_normalize_city", "customer_state"]].rename(
                    columns={
                        "customer_zip_code_prefix": "loc_code_prefix",
                        "customer_normalize_city": "city",
                        "customer_state": "uf",
                    }
                ),
                sellers[["seller_zip_code_prefix", "seller_normalize_city", "seller_state"]].rename(
                    columns={
                        "seller_zip_code_prefix": "loc_code_prefix",
                        "seller_normalize_city": "city",
                        "seller_state": "uf",
                    }
                ),
            ],
            ignore_index=True
        ).drop_duplicates(
            ["loc_code_prefix", "city", "uf"]
        )
    
    cities["cit_sta_uf"] = cities["cit_sta_id"].map(
        states.set_index("sta_id")["sta_uf"]
    )

    locations["loc_cit_id"] = (
        locations["city"] + "_" + locations["uf"]
    ).map(
        cities.set_index(
            cities["cit_normalize_name"] + "_" + cities["cit_sta_uf"]
        )["cit_id"]
    )

    locations.drop(columns=["city", "uf"])

    logger.info(f"Localidades preparados para carga ({len(locations)} registros)")

    return locations

@capture_error("prepare", table="customers")
def _prepare_customers(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando customers para carga")
    
    customers = datasets["customers"]
    
    customers = pd.concat(
            [
                customers[["customer_unique_id"]].rename(
                    columns={
                        "customer_unique_id": "cus_unique_id",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["cus_unique_id"])  

    logger.info(f"Customers preparados para carga ({len(customers)} registros)")

    return customers

@capture_error("prepare", table="sellers")
def _prepare_sellers(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando sellers para carga")
    
    sellers = datasets["sellers"]

    locations = loaded["locations"]
    cities = loaded["cities"]
    states = loaded["states"]
    
    sellers = pd.concat(
            [
                sellers[["seller_id", "seller_zip_code_prefix", "seller_normalize_city", "seller_state"]].rename(
                    columns={
                        "seller_id": "sel_external_id",
                        "seller_zip_code_prefix": "zip",
                        "seller_normalize_city": "city",
                        "seller_state": "state",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["sel_external_id"])  

    cities = cities.merge(
        states[["sta_id", "sta_uf"]],
        left_on="cit_sta_id",
        right_on="sta_id",
        how="left"
    )

    locations = locations.merge(
        cities[["cit_id", "cit_normalize_name", "sta_uf"]],
        left_on="loc_cit_id",
        right_on="cit_id",
        how="left"
    )

    sellers = sellers.merge(
        locations[["loc_id", "loc_code_prefix", "cit_normalize_name", "sta_uf"]],
        left_on=["zip", "city", "state"],
        right_on=["loc_code_prefix", "cit_normalize_name", "sta_uf"],
        how="inner"
    )

    sellers = sellers.rename(
        columns={
            "loc_id": "sel_loc_id"
        }
    )

    logger.info(f"Sellers preparados para carga ({len(sellers)} registros)")

    return sellers[
        [
            "sel_external_id",
            "sel_loc_id"
        ]
    ]

@capture_error("prepare", table="categories")
def _prepare_categories(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando categories para carga")
    
    categories = datasets["categories"]
    products = datasets["products"]
    
    categories = pd.concat(
            [
                categories[["product_category_name", "product_category_name_english"]].rename(
                    columns={
                        "product_category_name": "cat_name",
                        "product_category_name_english": "cat_name_english",
                    }
                ),
                products[["product_category_name"]].rename(
                    columns={
                        "product_category_name": "cat_name",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["cat_name"])  

    logger.info(f"Categories preparados para carga ({len(categories)} registros)")

    return categories

@capture_error("prepare", table="products")
def _prepare_products(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando products para carga")
    
    products = datasets["products"]

    categories = loaded["categories"]
    
    products = pd.concat(
            [
                products[["product_id", "product_category_name", "product_photos_qty", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]].rename(
                    columns={
                        "product_id": "pro_external_id",
                        "product_category_name": "category",
                        "product_photos_qty": "pro_photo_count",
                        "product_weight_g": "pro_weight",
                        "product_length_cm": "pro_length",
                        "product_height_cm": "pro_height",
                        "product_width_cm": "pro_width",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["pro_external_id"])  

    products = products.merge(
        categories[["cat_id", "cat_name"]],
        left_on="category",
        right_on="cat_name",
        how="inner"
    ).rename(
        columns={
            "cat_id": "pro_cat_id"
        }
    )

    products["pro_cat_id"] = products["pro_cat_id"].astype("int64")

    products = products.drop(columns=["category", "cat_name"])

    logger.info(f"Products preparados para carga ({len(products)} registros)")

    return products

@capture_error("prepare", table="orders")
def _prepare_orders(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando orders para carga")
    
    orders = datasets["orders"]
    customersraw = datasets["customers"]

    customers = loaded["customers"]
    locations = loaded["locations"]
    cities = loaded["cities"]
    states = loaded["states"]
    
    orders = pd.concat(
            [
                orders[["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]].rename(
                    columns={
                        "order_id": "ord_external_id",
                        "customer_id": "ord_customer_external_id",
                        "order_status": "ord_status",
                        "order_purchase_timestamp": "ord_purchase_date",
                        "order_approved_at": "ord_approved_at",
                        "order_delivered_carrier_date": "ord_shipped_at",
                        "order_delivered_customer_date": "ord_delivered_at",
                        "order_estimated_delivery_date": "ord_estimated_delivery_date",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["ord_external_id"])

    orders = orders.merge(
        customersraw[["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_normalize_city", "customer_state"]],
        left_on="ord_customer_external_id",
        right_on="customer_id",
        how="inner"
    )

    orders = orders.merge(
        customers[["cus_id", "cus_unique_id"]],
        left_on="customer_unique_id",
        right_on="cus_unique_id",
        how="inner"
    ).rename(
        columns={
            "cus_id": "ord_cus_id"
        }
    )

    cities = cities.merge(
        states[["sta_id", "sta_uf"]],
        left_on="cit_sta_id",
        right_on="sta_id",
        how="left"
    )

    locations = locations.merge(
        cities[["cit_id", "cit_normalize_name", "sta_uf"]],
        left_on="loc_cit_id",
        right_on=["cit_id"],    
        how="left"
    )

    orders = orders.merge(
        locations[["loc_id", "loc_code_prefix", "cit_normalize_name", "sta_uf"]],
        left_on=["customer_zip_code_prefix", "customer_normalize_city", "customer_state"],
        right_on=["loc_code_prefix", "cit_normalize_name", "sta_uf"],
        how="inner"
    ).rename(
        columns={
            "loc_id": "ord_loc_id"
        }
    )

    logger.info(f"Orders preparados para carga ({len(orders)} registros)")

    return orders[[
        "ord_external_id", 
        "ord_status", 
        "ord_purchase_date", 
        "ord_approved_at", 
        "ord_shipped_at", 
        "ord_delivered_at", 
        "ord_estimated_delivery_date",
        "ord_cus_id",
        "ord_customer_external_id",
        "ord_loc_id"
    ]]

@capture_error("prepare", table="order_items")
def _prepare_order_items(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando order_items para carga")

    order_items = datasets["order_items"]

    sellers = loaded["sellers"]
    products = loaded["products"]
    orders = loaded["orders"]

    order_items = pd.concat(
            [
                order_items[["order_item_id", "order_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"]].rename(
                    columns={
                        "order_item_id": "ori_external_id",
                        "order_id": "order_external_id",
                        "product_id": "product_external_id",
                        "seller_id": "seller_external_id",
                        "shipping_limit_date": "ori_shipment_limit_date",
                        "price": "ori_price",
                        "freight_value": "ori_freight_value",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["ori_external_id"])

    order_items = order_items.merge(
        orders[["ord_id", "ord_external_id"]],
        left_on="order_external_id",
        right_on="ord_external_id",
        how="inner"
    ).rename(
        columns={
            "ord_id": "ori_ord_id"
        }
    )

    order_items = order_items.merge(
        products[["pro_id", "pro_external_id"]],
        left_on="product_external_id",
        right_on="pro_external_id",
        how="inner"
    ).rename(
        columns={
            "pro_id": "ori_pro_id"
        }
    )

    order_items = order_items.merge(
        sellers[["sel_id", "sel_external_id"]],
        left_on="seller_external_id",
        right_on="sel_external_id",
        how="inner"
    ).rename(
        columns={
            "sel_id": "ori_sel_id"
        }
    )

    logger.info(f"Order_items items preparados para carga ({len(order_items)} registros)")

    return order_items[[
        "ori_external_id",
        "ori_ord_id",
        "ori_pro_id",
        "ori_sel_id",
        "ori_shipment_limit_date",
        "ori_price",
        "ori_freight_value"
    ]]

@capture_error("prepare", table="payments")
def _prepare_payments(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando payments para carga")

    payments = datasets["payments"]

    orders = loaded["orders"]

    payments = pd.concat(
            [
                payments[["order_id", "payment_sequential", "payment_type", "payment_installments"]].rename(
                    columns={
                        "order_id": "order_external_id",
                        "payment_sequential": "pay_sequential",
                        "payment_type": "pay_type",
                        "payment_installments": "pay_installments",
                    }
                )
            ],
            ignore_index=True
        )

    payments = payments.merge(
        orders[["ord_id", "ord_external_id"]],
        left_on="order_external_id",
        right_on="ord_external_id",
        how="inner"
    ).rename(
        columns={
            "ord_id": "pay_ord_id"
        }
    )

    logger.info(f"Payments items preparados para carga ({len(payments)} registros)")

    return payments[[
        "pay_ord_id",
        "pay_sequential",
        "pay_type",
        "pay_installments",
    ]]

@capture_error("prepare", table="reviews")
def _prepare_reviews(datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]):
    logger.info("Preparando reviews para carga")

    reviews = datasets["reviews"]

    orders = loaded["orders"]

    reviews = pd.concat(
            [
                reviews[["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message", "review_creation_date", "review_answer_timestamp"]].rename(
                    columns={
                        "review_id": "rev_external_id",
                        "order_id": "order_external_id",
                        "review_score": "rev_score",
                        "review_comment_title": "rev_title",
                        "review_comment_message": "rev_comment",
                        "review_creation_date": "rev_creation_at",
                        "review_answer_timestamp": "rev_answered_at",
                    }
                )
            ],
            ignore_index=True
        ).drop_duplicates(["rev_external_id"])

    reviews = reviews.merge(
        orders[["ord_id", "ord_external_id"]],
        left_on="order_external_id",
        right_on="ord_external_id",
        how="inner"
    ).rename(
        columns={
            "ord_id": "rev_ord_id"
        }
    )

    logger.info(f"Reviews items preparados para carga ({len(reviews)} registros)")

    return reviews[[
        "rev_external_id",
        "rev_ord_id",
        "rev_score",
        "rev_title",
        "rev_comment",
        "rev_creation_at",
        "rev_answered_at"
    ]]
                      
class SQLPrepareData(PrepareData):
    PREPARE_FUNCTIONS = {
        "cities": _prepare_cities,
        "locations": _prepare_locations,
        "customers": _prepare_customers,
        "sellers": _prepare_sellers,
        "categories": _prepare_categories,
        "products": _prepare_products,
        "orders": _prepare_orders,
        "order_items": _prepare_order_items,
        "payments": _prepare_payments,
        "reviews": _prepare_reviews,
    }

    def __init__(self, existing_tables):
        super().__init__(
            existing_tables=existing_tables,
            table_requirements=build_table_requirements(
                TABLE_MODELS
            )
        )