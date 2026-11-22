import main
from config import PROMPT_SISTEMA
from services.gemini_service import construir_instruccion


def test_sin_contexto_devuelve_solo_el_prompt_base():
    assert construir_instruccion(None) == PROMPT_SISTEMA
    assert construir_instruccion([]) == PROMPT_SISTEMA


def test_con_contexto_incluye_los_mensajes_previos():
    contexto = [
        {
            "fecha": "2026-11-21T10:00:00",
            "rol": "usuario",
            "contenido": "Me llamo Jose",
        },
        {
            "fecha": "2026-11-21T10:00:05",
            "rol": "asistente",
            "contenido": "Mucho gusto, Jose",
        },
    ]

    instruccion = construir_instruccion(contexto)

    assert PROMPT_SISTEMA in instruccion
    assert "[2026-11-21] Usuario: Me llamo Jose" in instruccion
    assert "[2026-11-21] Asistente: Mucho gusto, Jose" in instruccion


def test_cargar_contexto_omite_las_despedidas(monkeypatch):
    historial = [
        {"fecha": "2026-11-21T10:00:00", "rol": "usuario", "contenido": "Hola"},
        {
            "fecha": "2026-11-21T10:00:05",
            "rol": "asistente",
            "contenido": "Hola, ¿qué tal?",
        },
        {"fecha": "2026-11-21T10:00:00", "rol": "usuario", "contenido": "Adiós."},
    ]
    monkeypatch.setattr(main, "obtener_historial", lambda limite: historial)

    contexto = main.cargar_contexto()

    assert [m["contenido"] for m in contexto] == ["Hola", "Hola, ¿qué tal?"]
