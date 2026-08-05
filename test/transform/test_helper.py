import pandas as pd
import pytest

from src.transform.helper import (
    normalize_nulls,
    validate_columns,
    validate_required_values
)


def test_normalize_nulls():

    df = pd.DataFrame({
        "coluna": [
            "",
            " ",
            "NULL",
            "null",
            "NaN",
            "nan",
            "N/A",
            "valor"
        ]
    })

    result = normalize_nulls(df)

    assert result["coluna"].isna().sum() == 7
    assert result["coluna"].iloc[-1] == "valor"


def test_validate_columns_success():

    df = pd.DataFrame({
        "id": [1],
        "nome": ["Ana"]
    })

    # Não deve lançar erro
    validate_columns(
        df,
        required_columns=[
            "id",
            "nome"
        ],
        table_name="customers"
    )


def test_validate_columns_missing():

    df = pd.DataFrame({
        "id": [1]
    })

    with pytest.raises(ValueError):
        validate_columns(
            df,
            required_columns=[
                "id",
                "nome"
            ],
            table_name="customers"
        )


def test_validate_required_values_remove_nulls():

    df = pd.DataFrame({
        "id": [1, 2, 3],
        "name": [
            "Ana",
            None,
            "João"
        ]
    })

    result = validate_required_values(
        df,
        required_columns=[
            "id",
            "name"
        ],
        table_name="customers"
    )

    assert len(result) == 2
    assert result["name"].isna().sum() == 0