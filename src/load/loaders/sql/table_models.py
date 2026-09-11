from src.database.models import (
    Cities,
    Customers,
    Sellers,
    Products,
    Orders,
    OrderItems,
    Payments,
    Reviews,
    States,
    Locations,
    Categories,
)


TABLE_MODELS = {
    "states": States,
    "cities": Cities,
    "locations": Locations,
    "customers": Customers,
    "sellers": Sellers,
    "categories": Categories,
    "products": Products,
    "orders": Orders,
    "order_items": OrderItems,
    "payments": Payments,
    "reviews": Reviews,
}

def build_table_requirements(table_models):
    requirements = {}

    for table_name, model in table_models.items():
        required_tables = set()

        for foreign_key in model.__table__.foreign_keys:
            required_table = foreign_key.column.table.name

            required_tables.add(required_table)

        requirements[table_name] = {
            "load": False,
            "required_tables": required_tables
        }

    return requirements