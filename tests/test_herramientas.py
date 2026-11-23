from tools import HERRAMIENTAS
from tools.calculadora import calcular
from tools.tiempo import obtener_fecha_hora


def test_las_herramientas_estan_registradas():
    nombres = {h.__name__ for h in HERRAMIENTAS}
    assert {"calcular", "obtener_fecha_hora"} <= nombres


def test_cada_herramienta_tiene_descripcion():
    for herramienta in HERRAMIENTAS:
        assert herramienta.__doc__


def test_calcular_operaciones_basicas():
    assert calcular("12 * (3 + 4)") == {"resultado": 84}
    assert calcular("10 / 4") == {"resultado": 2.5}
    assert calcular("-5 + 2") == {"resultado": -3}


def test_calcular_rechaza_codigo_peligroso():
    resultado = calcular("__import__('os').system('dir')")
    assert "error" in resultado


def test_calcular_rechaza_exponentes_enormes():
    assert "error" in calcular("9 ** 9 ** 9")


def test_calcular_division_por_cero_devuelve_error():
    assert "error" in calcular("1 / 0")


def test_fecha_hora_tiene_los_campos_esperados():
    datos = obtener_fecha_hora()
    assert set(datos) == {"dia_semana", "fecha", "hora"}
    assert len(datos["hora"]) == 5
