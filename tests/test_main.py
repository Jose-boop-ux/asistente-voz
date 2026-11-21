import main

class CerebroFalso:
    def responder(self, texto= str) ->str:
        return f"Eco: {texto}"
    

def preparar(monkeypatch, texto_transcrito: str):
    """Remplaza micrófono, voz y base de datos por versiones falsas."""
    dichas = []
    guardados = []
    monkeypatch.setattr(main, "grabar", lambda segundos: b"")
    monkeypatch.setattr(main, "transcribir", lambda audio: texto_transcrito)
    monkeypatch.setattr(main, "hablar", dichas.append)
    monkeypatch.setattr(
        main, "guardar_mensaje", lambda sesion, rol, texto: guardados.append((rol, texto))
    )    
    return dichas, guardados


def test_conversasion_normal_responde_y_guarda(monkeypatch):
    dichas, guardados = preparar(monkeypatch, "Hola")
    
    continuar = main.procesar_turno(CerebroFalso(), 1)
    
    assert continuar is True 
    assert dichas == ["Eco: Hola"]
    assert guardados == [("usuario", "Hola"), ("asistente", "Eco: Hola")]
    
    
def test_palabra_de_salida_termina_la_conversacion(monkeypatch):
    dichas, _ = preparar(monkeypatch, "Adiós.")
    
    continuar = main.procesar_turno(CerebroFalso(), 1)
    
    assert continuar is False
    assert dichas == ["Hasta luego."]
    
    
def test_silencio_no_responde_ni_guarda(monkeypatch):
    dichas, guardados = preparar(monkeypatch, "")
    
    continuar = main.procesar_turno(CerebroFalso(), 1)
    
    assert continuar is True
    assert dichas == []
    assert guardados == []            