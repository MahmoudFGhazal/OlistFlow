

from src.database.models import States
from src.load.loaders.sql.sql_loader import SQLLoader

class PostgreLoader(SQLLoader):
    def __init__(self, engine):
        super().__init__(
            name="PostgreSQL",
            existing_tables={
                "states": States
            },
            engine=engine
        )
