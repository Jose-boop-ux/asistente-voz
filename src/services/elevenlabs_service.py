import io

import numpy as np
import sounddevice as sd
from elevenlabs.client import ElevenLabs

from config import (
    ELEVENLABS_API_KEY,
    STT_MODEL_ID,
    TTS_MODEL_ID,
    TTS_SAMPLE_RATE,
    VOICE_ID,
)

_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def transcribir(audio_wav: bytes) -> str:
    """Convierte audio WAV en texto (español)."""
    resultado = _client.speech_to_text.convert(
        file=io.BytesIO(audio_wav),
        model_id=STT_MODEL_ID,
        language_code="spa",
    )
    return resultado.text.strip()


def hablar(texto: str) -> None:
    """Convierte texto en voz y lo reproduce."""
    audio = _client.text_to_speech.convert(
        text=texto,
        voice_id=VOICE_ID,
        model_id=TTS_MODEL_ID,
        output_format="pcm_24000",
    )
    datos = b"".join(audio)
    muestras = np.frombuffer(datos, dtype=np.int16)
    sd.play(muestras, samplerate=TTS_SAMPLE_RATE)
    sd.wait()
