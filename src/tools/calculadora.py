import ast
import operator

from tools.registro import herramienta

_OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

MAX_EXPONENTE = 100


def _evaluar(nodo):
    """Evalúa solo números y operaciones aritméticas; rechaza todo lo demás."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return nodo.value

    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
        izquierda = _evaluar(nodo.left)
        derecha = _evaluar(nodo.right)
        if isinstance(nodo.op, ast.Pow) and abs(derecha) > MAX_EXPONENTE:
            raise ValueError("El exponente es demasiado grande")
        return _OPERADORES[type(nodo.op)](izquierda, derecha)

    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _OPERADORES:
        return _OPERADORES[type(nodo.op)](_evaluar(nodo.operand))

    raise ValueError("Expresión no permitida")


@herramienta
def calcular(expresion: str) -> dict:
    """Calcular una operación aritmética con +, -, *, /, ** y %.

    Úsala para cualquier cuenta matemática en vez de calcular de cabeza.

    Args:
        expresion: La operación a calcular, por ejemplo "12 * (3 + 4)".
    """
    arbol = ast.parse(expresion, mode="eval")
    return {"resultado": _evaluar(arbol.body)}
