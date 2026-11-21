from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)
respuesta = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Salúdame en una frase corta en español.",
    
)
print(respuesta.text)