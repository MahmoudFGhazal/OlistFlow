import pandas as pd

from src.extract.excel_reader import read_file, extract_dataset


def test_read_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test")

    result = read_file(file)

    assert result is None

def test_extract_dataset(tmp_path):
    csv = tmp_path / "clientes.csv"

    df = pd.DataFrame({
        "id": [1, 2],
        "nome": ["Ana", "João"]
    })

    df.to_csv(csv, index=False)

    datasets = extract_dataset(tmp_path)

    assert "clientes" in datasets
    assert len(datasets["clientes"]) == 2