import pytest

from src.errors import capture_error


def test_capture_error_success():

    @capture_error(
        stage="TEST",
        table="example"
    )
    def function_success():

        return "ok"


    result = function_success()


    assert result == "ok"



def test_capture_error_failure():

    @capture_error(
        stage="TEST",
        table="example"
    )
    def function_error():

        raise ValueError(
            "erro"
        )


    with pytest.raises(ValueError):

        function_error()