from evaluaciones.evaluar_estabilidad import evaluar_estabilidad
from evaluaciones.evaluar_posicion import evaluar_posicion
from evaluaciones.evaluar_movimiento import evaluar_movimiento
from evaluaciones.evaluar_contacto import evaluar_contacto
from evaluaciones.evaluar_seguimiento import evaluar_seguimiento

def evaluar_saque(landmarks):
    """
    Evalúa el saque de un jugador basado en los puntos de referencia del cuerpo.
    
    Args:
        landmarks: Lista de puntos de referencia del cuerpo.
    
    Returns:
        str: Resultados de la evaluación del saque.
    """
    try:
        # Evaluar cada aspecto del saque
        resultado_posicion = evaluar_posicion(landmarks)
        resultado_movimiento = evaluar_movimiento(landmarks)
        resultado_contacto = evaluar_contacto(landmarks)
        resultado_seguimiento = evaluar_seguimiento(landmarks)
        resultado_estabilidad = evaluar_estabilidad(landmarks)

        # Combinar resultados
        resultados = [
            resultado_posicion,
            resultado_movimiento,
            resultado_contacto,
            resultado_seguimiento,
            resultado_estabilidad
        ]

        # Retornar todos los resultados
        return "\n".join(resultados)
    except Exception as e:
        return f"Error al evaluar el saque: {e}"