import sqlite3

import pytest

from database import db


@pytest.fixture(autouse=True)
def bd_temporal(tmp_path, monkeypatch):
    """Cada prueba usa una base de datos temporal, nunca real."""
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "prueba.db")
    db.iniciar_bd()


def test_crear_sesion_devuelve_ids_consecutivos():
    primero = db.crear_sesion()
    segundo = db.crear_sesion()
    assert segundo == primero + 1


def test_guardar_y_leer_mensajes():
    sesion = db.crear_sesion()
    db.guardar_mensaje(sesion, "usuario", "Hola")
    db.guardar_mensaje(sesion, "asistente", "¡Hola! ¿Cómo estás?")

    historial = db.obtener_historial()

    assert len(historial) == 2
    assert historial[0]["rol"] == "usuario"
    assert historial[1]["contenido"] == "¡Hola! ¿Cómo estás?"


def test_historial_respeta_el_limite():
    sesion = db.crear_sesion()
    for i in range(5):
        db.guardar_mensaje(sesion, "usuario", f"mensaje {i}")

    historial = db.obtener_historial(limite=3)

    contenidos = [m["contenido"] for m in historial]
    assert contenidos == ["mensaje 2", "mensaje 3", "mensaje 4"]


def test_rol_invalido_es_rechazado():
    sesion = db.crear_sesion()
    with pytest.raises(sqlite3.IntegrityError):
        db.guardar_mensaje(sesion, "robot", "Hola")


def test_mensaje_con_sesion_inexistente_es_rechazado():
    with pytest.raises(sqlite3.IntegrityError):
        db.guardar_mensaje(999, "usuario", "Hola")
