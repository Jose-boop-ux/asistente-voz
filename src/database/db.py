import sqlite3
from contextlib import contextmanager
from datetime import datetime

from config import DB_PATH

ESQUEMA = """
CREATE TABLE IF NOT EXISTS sesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inicio TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    sesion_id INTEGER NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('usuario', 'asistente')),
    contenido TEXT NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (sesion_id) REFERENCES sesiones(id) 
);
"""
@contextmanager
def _conectar():
    """Abre la conexion, confirma cambios y la cierra siempre."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
        
def _ahora()-> str:
    return datetime.now().isoformat(timespec="seconds")

def iniciar_bd()-> None:
    """Crea las tablas si todavía no existen."""
    with _conectar() as conexion: 
        conexion.executescript(ESQUEMA)
        
def crear_sesion()-> int:
    """Registra una nueva sesion y devuelve su id."""
    with _conectar() as conexion:
        cursor = conexion.execute(
            "INSERT INTO sesiones (inicio) VALUES (?)", 
            (_ahora(),),
        )
        return cursor.lastrowid

def guardar_mensaje(sesion_id: int, rol: str, contenido: str) ->None:
    """Guardar un mensaje del usuario o del asistente."""
    with _conectar() as conexion:
        conexion.execute(
            "INSERT INTO mensajes (sesion_id, rol, contenido, fecha)"
            "VALUES (?, ?, ?, ?)",
            (sesion_id, rol, contenido, _ahora()),
        )    

def obtener_historial(limite: int = 20) -> list[dict]:
            """Devuelve los últimos mensajes, del mas antiguo al mas reciente."""
            with _conectar() as conexion:
                filas = conexion.execute(
                    "SELECT sesion_id, rol, contenido, fecha FROM mensajes "
                    "ORDER BY id DESC LIMIT ?",
                    (limite,),
                ).fetchall()
            return [dict(fila) for fila in reversed(filas)]    