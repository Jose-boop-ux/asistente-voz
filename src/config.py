import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.5-flash"
STT_MODEL_ID = "scribe_v2"
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "asistente.db"
TTS_MODEL_ID = "eleven_multilingual_v2"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
TTS_SAMPLE_RATE = 24000
MAX_SEGUNDOS_ESPERA = 8
MAX_SEGUNDOS_GRABACION = 20
SEGUNDOS_SILENCIO = 1.0
UMBRAL_MINIMO = 600

PROMPT_SISTEMA = (
    "Eres un asistente de voz amable que habla español. "
    "Responde de forma breve y natural, en maximo de frases. "
    "No uses listas, emojis ni formato especial, "
    "porque tus respuestas se leerán en voz alta. "
)

if not ELEVENLABS_API_KEY:
    raise RuntimeError("Falta ELEVENLABS_API_KEY. Revisa tu archivo .env")

if not GEMINI_API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY. Revisa tu archivo .env")
