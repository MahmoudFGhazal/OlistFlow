from src.errors import handle_error


def test_handle_error():

    error = ValueError(
        "erro teste"
    )

    result = handle_error(
        error,
        stage="TRANSFORM",
        table="customers"
    )


    assert result["stage"] == "TRANSFORM"

    assert result["table"] == "customers"

    assert result["error_type"] == "ValueError"

    assert result["message"] == "erro teste"