import numpy as np 
import sounddevice as sd
from elevenlabs.client import ElevenLabs

from config import ELEVENLABS_API_KEY

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
MODEL_ID = "eleven_multilingual_v2"
SAMPLE_RATE = 24000


def hablar(texto: str) -> None:
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=texto,
        voice_id=VOICE_ID,
        model_id=MODEL_ID,
        output_format="pcm_24000"
    )
    datos = b"".join(audio)
    muestras = np.frombuffer(datos, dtype=np.int16)
    sd.play(muestras, samplerate=SAMPLE_RATE)
    sd.wait()
    
if __name__== "__main__":
    hablar("Hola Jose, soy tu asistente de voz. Ya estoy funcionando.")    
    