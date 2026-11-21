from database.db import iniciar_bd, obtener_historial

iniciar_bd()
mensajes = obtener_historial(20)

if not mensajes:
    print("Todavía no hay mensaje guardados.")
    
for m in mensajes:
    print(f"[{m['fecha']}] {m['rol']}: {m['contenido']}")    