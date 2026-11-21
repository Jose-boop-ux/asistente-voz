from audio.microfono import grabar
from config import SEGUNDOS_GRABACION
from services.elevenlabs_service import hablar, transcribir
from services.gemini_service import Cerebro

PALABRAS_SALIDA = {"salir", "adiós", "adios", "chao", "hasta luego"}

def main() -> None:
    cerebro = Cerebro()
    hablar("Hola, soy tu asistente de voz. ¿En qué te puedo ayudar?")
    
    while True:
        audio = grabar(SEGUNDOS_GRABACION)
        texto = transcribir(audio)
        
        if not texto:
            print("No te escuché, intenta de nuevo.")
            continue
        
        print(f"Tú: {texto}")
        
        if texto.lower().strip(" .,!¡¿?") in PALABRAS_SALIDA:
            hablar("Hasta luego.")
            break
        
        respuesta = cerebro.responder(texto)
        print(f"Asistente: {respuesta}")
        hablar(respuesta)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAsistente detenido.")        