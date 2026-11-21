from audio.microfono import grabar
from config import SEGUNDOS_GRABACION
from database.db import crear_sesion, guardar_mensaje, iniciar_bd
from services.elevenlabs_service import hablar, transcribir
from services.gemini_service import Cerebro

PALABRAS_SALIDA = {"salir", "adiós", "adios", "chao", "hasta luego"}

def main() -> None:
    iniciar_bd()
    sesion_id = crear_sesion()
    cerebro = Cerebro()
    hablar("Hola, soy tu asistente de voz. ¿En qué te puedo ayudar?")
    
    while True:
        audio = grabar(SEGUNDOS_GRABACION)
        texto = transcribir(audio)
        
        if not texto:
            print("No te escuché, intenta de nuevo.")
            continue
        
        print(f"Tú: {texto}")
        guardar_mensaje(sesion_id, "usuario", texto)
        
        if texto.lower().strip(" .,!¡¿?") in PALABRAS_SALIDA:
            hablar("Hasta luego.")
            break
        
        respuesta = cerebro.responder(texto)
        print(f"Asistente: {respuesta}")
        guardar_mensaje(sesion_id, "asistente", respuesta)
        hablar(respuesta)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAsistente detenido.")        