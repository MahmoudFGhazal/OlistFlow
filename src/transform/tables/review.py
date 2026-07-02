import logging
import pandas as pd

from ..helper import validate_columns, validate_required_values

"""
review_id* string
order_id* string
review_score* integer
review_comment_title string
review_comment_message string
review_creation_date* datetime
review_answer_timestamp datetime

sem duplicatas
"""

TABLE_NAME="reviews"

REVIEW_ID = "review_id"
ORDER_ID = "order_id"
REVIEW_SCORE = "review_score"
REVIEW_COMMENT_TITLE = "review_comment_title"
REVIEW_COMMENT_MESSAGE = "review_comment_message"
REVIEW_CREATION_DATE = "review_creation_date"
REVIEW_ANSWER_TIMESTAMP = "review_answer_timestamp"

COLUMNS = [
    REVIEW_ID,
    ORDER_ID,
    REVIEW_SCORE,
    REVIEW_COMMENT_TITLE,
    REVIEW_COMMENT_MESSAGE,
    REVIEW_CREATION_DATE,
    REVIEW_ANSWER_TIMESTAMP,
]

REQUIRED_COLUMNS = [
    REVIEW_ID,
    ORDER_ID,
    REVIEW_SCORE,
    REVIEW_CREATION_DATE,
]

logger = logging.getLogger(f"etl.transform.{TABLE_NAME}")

def transform_reviews(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Transformando {TABLE_NAME}")

    validate_columns(
        df,
        required_columns=COLUMNS,
        table_name=TABLE_NAME
    )

    df = _clean_reviews(df)

    df = validate_required_values(
        df,
        required_columns=REQUIRED_COLUMNS,
        table_name=TABLE_NAME
    )

    df = df.drop_duplicates(
        subset=[
            REVIEW_ID
        ]
    )

    logger.info(f"{TABLE_NAME.capitalize()} transformada ({len(df)} registros)")

    return df


def _clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Limpando {TABLE_NAME}")

    df = df.copy()

    STRING_COLUMNS = [
        REVIEW_ID,
        ORDER_ID,
    ]

    for column in STRING_COLUMNS:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    df[REVIEW_SCORE] = pd.to_numeric(
        df[REVIEW_SCORE],
        errors="coerce"
    ).astype("Int64")

    TEXT_COLUMNS = [
        REVIEW_COMMENT_TITLE,
        REVIEW_COMMENT_MESSAGE,
    ]

    for column in TEXT_COLUMNS:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    DATETIME_COLUMNS = [
        REVIEW_CREATION_DATE,
        REVIEW_ANSWER_TIMESTAMP,
    ]

    for column in DATETIME_COLUMNS:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df