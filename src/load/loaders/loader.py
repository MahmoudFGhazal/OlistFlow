

from abc import ABC, abstractmethod
import logging
from typing import Any

import pandas as pd
from sqlalchemy import select

from src.errors.decorator import capture_error
from src.load.loaders.prepare_data import PrepareData


class Loader(ABC):
    def __init__(self, name: str, engine, existing_tables: dict[str, Any]):
        self.logger = logging.getLogger(__name__)

        self.database_name = name
        self.engine = engine
        self.existing_tables = existing_tables
    
    @abstractmethod
    def create_prepare_data(self) -> PrepareData:
        pass

    @abstractmethod
    def load_existing_data(self, connection):
        pass

    @abstractmethod
    def insert(self, connection, data):
        pass

    @abstractmethod
    def connection(self):
        pass

    @capture_error("load")
    def load(self, data):
        self.logger.info(f"Carga de dados no {self.database_name}")

        prepare_data = self.create_prepare_data()

        with self.connection() as connection:
            loaded = self.load_existing_data(connection)

            stagnant_rounds = 0
            max_stagnant_rounds = 3

            while not prepare_data.all_loaded():
                prepared_data = prepare_data.prepare_for_load(data, loaded)

                if not prepared_data:
                    stagnant_rounds += 1

                    if stagnant_rounds >= max_stagnant_rounds:
                        pending = prepare_data.pending_tables()

                        self.logger.error(
                            f"Nenhuma tabela nova foi carregada em {stagnant_rounds} iterações seguidas. "
                            f"Tabelas pendentes: {pending}"
                        )
                        raise RuntimeError(
                            f"Carga travada — tabelas não resolvidas: {pending}"
                        )
                else:
                    stagnant_rounds = 0

                data_loaded = self.insert(
                    connection,
                    prepared_data
                )

                loaded.update(data_loaded)

                prepare_data.mark_loaded(
                    data_loaded.keys()
                )
