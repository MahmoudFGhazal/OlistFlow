


import pandas as pd
from sqlalchemy import select

from src.load.loaders.loader import Loader
from src.load.loaders.sql.sql_insert import SQLInsert
from src.load.loaders.sql.sql_prepare_data import SQLPrepareData


class SQLLoader(Loader):
    def __init__(
        self,
        name,
        existing_tables,
        engine,
        inserter = SQLInsert()
    ):
        super().__init__(
            name=name,
            existing_tables=existing_tables,
            engine=engine
        )

        self.inserter = inserter

    def connection(self):
        return self.engine.begin()

    def create_prepare_data(self):
        return SQLPrepareData(existing_tables=self.existing_tables)

    def insert(self, connection, data):
        return self.inserter.execute(
            connection,
            data
        )

    def load_existing_data(self, connection):
        loaded = {}

        for name, model in self.existing_tables.items():
            res = connection.execute(select(model))

            loaded[name] = pd.DataFrame(res.mappings().all())

        return loaded

