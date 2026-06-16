import logging
from pathlib import Path
import pandas as pd

DATASET_PATH = Path("data/raw")

logger = logging.getLogger(__name__)

def read_file(file: Path):
    logger.info(f"Lendo arquivo: {file.name}")

    if file.suffix == ".csv":
        return pd.read_csv(file)
    
    raise ValueError(
        f"Tipo de arquivo não suportado: {file.suffix} "
        f"para o arquivo '{file.name}'"
    )

def extract_dataset(path: Path = DATASET_PATH):
    if not path.exists():
        raise FileNotFoundError(
            f"Pasta não encontrada: {DATASET_PATH}"
        )

    return {
        file.stem: read_file(file)
        for file in path.iterdir()
        if file.is_file()
    }
    