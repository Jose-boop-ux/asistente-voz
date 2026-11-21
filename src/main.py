from audio.microfono import grabar
from config import SEGUNDOS_GRABACION
from database.db import crear_sesion, guardar_mensaje, iniciar_bd
from logger import obtener_logger
from services.elevenlabs_service import hablar, transcribir
from services.gemini_service import Cerebro

log = obtener_logger("asistente")

PALABRAS_SALIDA = {"salir", "adiós", "adios", "chao", "hasta luego"}
MAX_ERRORES_SEGUIDOS = 3


def procesar_turno(cerebro: Cerebro, sesion_id: int) -> bool:
    """Ejecuta un turno completo. Devuelve False si el usuario quiere salir."""
    audio = grabar(SEGUNDOS_GRABACION)
    texto = transcribir(audio)

    if not texto:
        print("No te escuché, intenta de nuevo.")
        return True

    print(f"Tú: {texto}")
    guardar_mensaje(sesion_id, "usuario", texto)

    if texto.lower().strip(" .,!¡¿?") in PALABRAS_SALIDA:
        hablar("Hasta luego.")
        return False

    respuesta = cerebro.responder(texto)
    print(f"Asistente: {respuesta}")
    guardar_mensaje(sesion_id, "asistente", respuesta)
    hablar(respuesta)
    return True


def main() -> None:
    iniciar_bd()
    sesion_id = crear_sesion()
    log.info("Sesión %s iniciada", sesion_id)

    cerebro = Cerebro()
    hablar("Hola, soy tu asistente de voz. ¿En qué te puedo ayudar?")

    errores_seguidos = 0
    continuar = True

    while continuar:
        try:
            continuar = procesar_turno(cerebro, sesion_id)
            errores_seguidos = 0
        except Exception:
            errores_seguidos += 1
            log.exception("Error en el turno (%s seguidos)", errores_seguidos)
            print("Hubo un problema. Revisa tu conexion e intenta de nuevo.")
            if errores_seguidos >= MAX_ERRORES_SEGUIDOS:
                print("Demasiados errores seguidos. Cerrando el sistema.")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAsistente detenido.")
        log.info("Detenido por el usuario")
