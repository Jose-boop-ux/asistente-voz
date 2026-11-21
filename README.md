# Asistente de Voz con IA

Asistente de voz conversacional en español hecho con Python. Te escucha por el micrófono, genera una respuesta con inteligencia artificial y te contesta hablando. Cada conversación se guarda en una base de datos local.

## Cómo funciona

```
Micrófono → Voz a texto (ElevenLabs) → IA (Google Gemini) → Texto a voz (ElevenLabs) → Altavoz
                                                  ↓
                                         Historial (SQLite)
```

## Características

- Conversación por voz en español, con memoria durante la sesión.
- Historial de conversaciones guardado en SQLite.
- Manejo de errores: si falla la conexión, el asistente avisa y sigue funcionando.
- Registro de eventos con rotación de archivos (`logs/asistente.log`).
- Pruebas automáticas con pytest, sin gastar créditos ni usar el micrófono.
- Código formateado con black y revisado con ruff.

## Tecnologías

| Función | Herramienta |
| --- | --- |
| Lenguaje | Python 3.12 |
| Voz a texto y texto a voz | API de ElevenLabs |
| Generación de respuestas | API de Google Gemini |
| Audio | sounddevice, numpy |
| Base de datos | SQLite |
| Pruebas y calidad | pytest, black, ruff |

## Requisitos

- Python 3.10 o superior
- Micrófono y altavoces (o audífonos)
- Cuenta de ElevenLabs con una API key
- Cuenta de Google AI Studio con una API key de Gemini (hay capa gratuita)

## Instalación

```powershell
git clone https://github.com/Jose-boop-ux/asistente-voz.git
cd asistente-voz
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1. Copia la plantilla de variables de entorno:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Abre `.env` y escribe tus claves reales:

   ```
   ELEVENLABS_API_KEY=tu_clave_de_elevenlabs
   GEMINI_API_KEY=tu_clave_de_gemini
   ```

El archivo `.env` está en `.gitignore`, así que tus claves nunca se suben al repositorio.

## Uso

```powershell
python src\main.py
```

- Habla cuando aparezca "Escuchando... habla ahora".
- Para terminar, di "adiós", "chao" o "salir", o presiona `Ctrl + C`.

Para ver el historial guardado:

```powershell
python src\ver_historial.py
```

## Estructura del proyecto

```
asistente-voz/
├── src/
│ ├── main.py # punto de entrada y bucle de conversación
│ ├── config.py # configuración y variables de entorno
│ ├── logger.py # registro de eventos
│ ├── ver_historial.py # consulta del historial
│ ├── audio/
│ │ └── microfono.py # grabación del micrófono
│ ├── services/
│ │ ├── elevenlabs_service.py # voz a texto y texto a voz
│ │ └── gemini_service.py # respuestas de la IA
│ └── database/
│ └── db.py # SQLite: sesiones y mensajes
├── tests/ # pruebas automáticas
├── .env.example # plantilla de variables de entorno
├── pytest.ini
└── requirements.txt
```

## Pruebas y calidad del código

```powershell
pytest -v # pruebas automáticas
black src tests # formato
ruff check src tests # revisión de calidad
```

Las pruebas usan una base de datos temporal y reemplazan micrófono, voz e IA por versiones simuladas, así que no consumen créditos ni requieren internet.

## Privacidad y seguridad

- Las claves viven en `.env`, fuera del control de versiones.
- Las conversaciones se guardan solo en tu equipo (`data/asistente.db`).
- El audio y el texto se envían a ElevenLabs y a Google para procesarse, según los términos de cada servicio.
- El registro de eventos no incluye el contenido de las conversaciones.

## Limitaciones y mejoras futuras

- La grabación dura un tiempo fijo (5 segundos). Mejora prevista: detectar el silencio para terminar de grabar automáticamente.
- Reproducir el audio mientras se genera (streaming) para reducir la espera.
- Recuperar el contexto de conversaciones anteriores desde la base de datos.

## Licencia

Distribuido bajo la licencia MIT.