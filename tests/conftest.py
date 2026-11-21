import os

# Claves falsas para que config.py no exija el archivo .env en las pruebas.
os.environ.setdefault("ELEVENLABS_API_KEY", "clave-de-prueba")
os.environ.setdefault("GEMINI_API_KEY", "clave-de-prueba")
