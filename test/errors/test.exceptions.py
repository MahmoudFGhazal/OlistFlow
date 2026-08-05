from errors import (
    ETLError,
    ValidationError,
    ExtractionError,
    TransformationError,
    LoadError,
)


def test_custom_exceptions():

    assert issubclass(
        ValidationError,
        ETLError
    )

    assert issubclass(
        ExtractionError,
        ETLError
    )

    assert issubclass(
        TransformationError,
        ETLError
    )

    assert issubclass(
        LoadError,
        ETLError
    )