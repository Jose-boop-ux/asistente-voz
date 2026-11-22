import io
import wave
from collections import deque

import numpy as np
import sounddevice as sd

from config import (
    MAX_SEGUNDOS_ESPERA,
    MAX_SEGUNDOS_GRABACION,
    SEGUNDOS_SILENCIO,
    UMBRAL_MINIMO,
)

SAMPLE_RATE = 16000
BLOQUE_SEGUNDOS = 0.1
BLOQUE_MUESTRAS = int(SAMPLE_RATE * BLOQUE_SEGUNDOS)
BLOQUES_CALIBRACION = 3
BLOQUES_PREVIOS = 3


def _volumen(bloque: np.ndarray) -> float:
    """Calcula el volumen (RMS) de un bloque de audio."""
    return float(np.sqrt(np.mean(bloque.astype(np.float32) ** 2)))


def _a_wav(muestras: np.ndarray) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(muestras.tobytes())
    return buffer.getvalue()


def grabar() -> bytes | None:
    """Graba hasta que dejas de hablar.

    Devuelve el audio en formato WAV, o None si no se detectó voz.
    """
    print("Escuchando... habla ahora.")

    max_bloques_espera = int(MAX_SEGUNDOS_ESPERA / BLOQUE_SEGUNDOS)
    max_bloques_grabacion = int(MAX_SEGUNDOS_GRABACION / BLOQUE_SEGUNDOS)
    bloques_silencio_max = int(SEGUNDOS_SILENCIO / BLOQUE_SEGUNDOS)

    previos = deque(maxlen=BLOQUES_PREVIOS)
    grabado = []
    ruido = []
    umbral = UMBRAL_MINIMO
    hablando = False
    silencios = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=BLOQUE_MUESTRAS,
    ) as stream:
        for numero in range(max_bloques_espera + max_bloques_grabacion):
            datos, _ = stream.read(BLOQUE_MUESTRAS)
            bloque = datos[:, 0].copy()
            volumen = _volumen(bloque)

            # Primeros instantes: mide el ruido de fondo para ajustar el umbral.
            if numero < BLOQUES_CALIBRACION:
                ruido.append(volumen)
                previos.append(bloque)
                if numero == BLOQUES_CALIBRACION - 1:
                    umbral = max(UMBRAL_MINIMO, 3 * float(np.mean(ruido)))
                continue

            if not hablando:
                previos.append(bloque)
                if volumen > umbral:
                    hablando = True
                    grabado.extend(previos)
                elif numero >= max_bloques_espera:
                    return None
                continue

            grabado.append(bloque)
            silencios = silencios + 1 if volumen < umbral else 0
            if silencios >= bloques_silencio_max:
                break
            if len(grabado) >= max_bloques_grabacion:
                break

    if not hablando:
        return None

    print("Grabación terminada.")
    return _a_wav(np.concatenate(grabado))
