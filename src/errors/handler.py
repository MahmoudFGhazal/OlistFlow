import logging
import traceback
from datetime import datetime


logger = logging.getLogger("etl.error")


def handle_error(
    error: Exception,
    stage: str,
    table: str | None = None
):

    error_info = {
        "timestamp": datetime.now(),
        "stage": stage,
        "table": table,
        "error_type": type(error).__name__,
        "message": str(error),
    }


    logger.error(
        f"""
Erro no ETL
Etapa: {stage}
Tabela: {table}
Tipo: {error_info['error_type']}
Mensagem: {error_info['message']}
""",
        exc_info=True
    )


    return error_info