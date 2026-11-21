import logging
from logging.handlers import RotatingFileHandler

from config import BASE_DIR

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


def obtener_logger(nombre: str) -> logging.Logger:
    """Devuelve un logger que escribe en logs/asistente.log."""
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    archivo = RotatingFileHandler(
        LOG_DIR / "asistente_log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    archivo.setFormatter(formato)
    logger.addHandler(archivo)
    return logger