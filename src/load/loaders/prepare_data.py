
from abc import ABC
import logging
from typing import Any, Callable

import pandas as pd

from src.load.loaders.sql.table_models import build_table_requirements
from src.transform.types import TransformedDatasets


logger = logging.getLogger("etl.load.prepare_loader")

class PrepareData(ABC):
    PREPARE_FUNCTIONS: dict[str, Callable] = {}
    
    def __init__(self, existing_tables: dict[str, Any], table_requirements):
        self.table_requirements = table_requirements

        for table_name in existing_tables:
            self.table_requirements[table_name]["load"] = True

    def all_loaded(self ) -> bool:
        return all(
            table["load"]
            for table in self.table_requirements.values()
        )

    def pending_tables(self) -> list[str]:
        return [
            table_name
            for table_name, table in self.table_requirements.items()
            if not table["load"]
        ]

    def mark_loaded(self, table_names):
        for table_name in table_names:
            if table_name not in self.table_requirements:
                raise KeyError(
                    f"Tabela '{table_name}' não encontrada nos requisitos"
                )

            self.table_requirements[table_name]["load"] = True

    def prepare_for_load(self, datasets: TransformedDatasets, loaded: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        logger.info("Preparando datasets para carga")

        prepared = {}

        for table_name, table in self.table_requirements.items():
            if table["load"]:
                continue

            if not table["required_tables"].issubset(loaded.keys()):
                continue

            function = self.PREPARE_FUNCTIONS.get(table_name)

            if function is None:
                logger.warning(
                    f"Nenhuma função de preparação encontrada para {table_name}"
                )
                continue

            prepared[table_name] = function(
                datasets=datasets,
                loaded=loaded
            )

        return prepared