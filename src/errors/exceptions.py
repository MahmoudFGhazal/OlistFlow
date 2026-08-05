class ETLError(Exception):
    """Erro base do ETL"""
    pass


class ValidationError(ETLError):
    """Erro de validação dos dados"""
    pass


class ExtractionError(ETLError):
    """Erro durante extração"""
    pass


class TransformationError(ETLError):
    """Erro durante transformação"""
    pass


class LoadError(ETLError):
    """Erro durante carga"""
    pass