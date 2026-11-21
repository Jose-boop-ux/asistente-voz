from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, PROMPT_SISTEMA

_client = genai.Client(api_key=GEMINI_API_KEY)

class Cerebro:
    """Conversa con Gemini y recuerda lo dicho durante la sesión."""
    
    def __init__(self) -> None:
        self._chat = _client.chats.create(
            model=GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=PROMPT_SISTEMA
            ),
        )
       
    def responder(self, texto: str) -> str:
        respuesta = self._chat.send_message(texto)
        return respuesta.text.strip()    