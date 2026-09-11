

import pandas as pd
from sqlalchemy import insert

from .table_models import TABLE_MODELS

class SQLInsert:
    def __init__(self, batch_size=1000):
        self.batch_size = batch_size

    def execute(self, connection, data):
        loaded = {}

        for table_name, dataframe in data.items():
            model = TABLE_MODELS[table_name]

            records = dataframe.to_dict(orient="records")

            stmt = insert(model).returning(model)
            inserted_rows = []
    
            for i in range(0, len(records), self.batch_size):
                batch = records[i:i + self.batch_size]

                res = connection.execute(stmt, batch)

                inserted_rows.extend(res.mappings().all())

            loaded[table_name] = pd.DataFrame(inserted_rows)

        return loaded
    