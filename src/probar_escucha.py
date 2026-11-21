from audio.microfono import grabar
from services.elevenlabs_service import transcribir

audio = grabar(5)
texto = transcribir(audio)
print(f"Entendí: {texto}")
