


import logging

from src.errors.decorator import capture_error
from src.load.loaders.loader import Loader

logger = logging.getLogger("etl.load")

@capture_error("load")
def load_data(data, loader: Loader):
    logger.info("Iniciando carga de dados")

    loader.load(data)

    logger.info("Carga de dados concluída com sucesso")