import functools

from logger import obtener_logger

log = obtener_logger("herramientas")

HERRAMIENTAS = []


def herramienta(funcion):
    """Registra una función como herramienta del asistente.

    Anota cada uso en el log (sin los argumentos, por privacidad). Si la
    función falla, devuelve el error en lugar de cerrar el programa, para
    que el asistente pueda explicárselo al usuario.
    """

    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        log.info("Herramienta %s llamada", funcion.__name__)
        try:
            return funcion(*args, **kwargs)
        except Exception as error:
            log.exception("Falló la herramienta %s", funcion.__name__)
            return {"error": str(error)}

    HERRAMIENTAS.append(envoltura)
    return envoltura
