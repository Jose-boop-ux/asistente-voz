import io
import wave

import sounddevice as sd

SAMPLE_RATE = 16000

def grabar(segundos: int = 5) -> bytes:
    """Graba del micrófono y devuelve el audio en formato WAV."""
    print(f"Escuchando durante {segundos} segundos... habla ahora.")
    audio = sd.rec(
        int(segundos * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    print("Grabación terminada.")
    
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(audio.tobytes())
    return buffer.getvalue()    