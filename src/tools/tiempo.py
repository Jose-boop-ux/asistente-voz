from datetime import datetime

from tools.registro import herramienta

DIAS = [
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
]
MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


@herramienta
def obtener_fecha_hora() -> dict:
    """Devuelve el dia de la semana, la fecha y la hora actuales.

    Úsala cuando el usuario pregunte qué dia es, la fecha o la hora.
    """
    ahora = datetime.now()
    return {
        "dia_semana": DIAS[ahora.weekday()],
        "fecha": f"{ahora.day} de {MESES[ahora.month - 1]} de {ahora.year}",
        "hora": ahora.strftime("%H:%M"),
    }
