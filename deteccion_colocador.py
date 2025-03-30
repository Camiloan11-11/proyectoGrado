import cv2
import mediapipe as mp
import numpy as np
import csv

# Crear archivo CSV y escribir encabezados
with open('analisis_postura.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'Angulo Codo', 'Angulo Rodilla', 'Angulo Tronco', 'Manos Sobre Frente'])

# Inicializar Mediapipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def calcular_angulo(a, b, c):
    """
    Calcula el ángulo entre tres puntos.
    
    Args:
        a, b, c: Coordenadas de los puntos.
    
    Returns:
        float o None: Ángulo en grados o None si no se puede calcular.
    """
    if None in (a, b, c):  # Evita cálculos con datos inválidos
        return None

    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b

    # Verificar si los vectores son válidos antes de calcular el ángulo
    norm_ba, norm_bc = np.linalg.norm(ba), np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0:
        return None

    coseno_angulo = np.dot(ba, bc) / (norm_ba * norm_bc)
    angulo = np.arccos(np.clip(coseno_angulo, -1.0, 1.0))  # Evita errores numéricos
    return np.degrees(angulo)

def detectar_colocador(landmarks, frame_number):
    """
    Detecta la postura del colocador basado en los puntos de referencia del cuerpo.
    
    Args:
        landmarks: Lista de puntos de referencia del cuerpo.
        frame_number: Número del cuadro actual.
    
    Returns:
        str: Evaluación de la postura.
    """
    try:
        # Extraer coordenadas necesarias (verificamos que existan)
        puntos = [
            mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_EYE, mp_pose.PoseLandmark.RIGHT_EYE
        ]

        if any(landmarks[p] is None for p in puntos):
            return "❌ No se detectaron todos los puntos necesarios"

        hombro_izq = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
        codo_izq = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
        muñeca_izq = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]
        
        cadera_izq = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
        rodilla_izq = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
        tobillo_izq = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
        
        ojo_izq = [landmarks[mp_pose.PoseLandmark.LEFT_EYE].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE].y]
        ojo_der = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE].y]
        ojos = [(ojo_izq[0] + ojo_der[0]) / 2, (ojo_izq[1] + ojo_der[1]) / 2]

        manos_sobre_frente = muñeca_izq[1] < ojos[1]
        
        # Calcular ángulos
        angulo_codo = calcular_angulo(hombro_izq, codo_izq, muñeca_izq)
        angulo_rodilla = calcular_angulo(cadera_izq, rodilla_izq, tobillo_izq)
        
        cadera_der = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
        hombro_der = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
        angulo_tronco = calcular_angulo(cadera_der, hombro_der, ojos)

        # Evitar escritura de datos inválidos
        if None in (angulo_codo, angulo_rodilla, angulo_tronco):
            return "❌ No se pudieron calcular todos los ángulos"

        # Guardar datos en el CSV
        with open('analisis_postura.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([frame_number, angulo_codo, angulo_rodilla, angulo_tronco, manos_sobre_frente])

        # Evaluación de la postura
        evaluacion = [
            "✅ Codo correcto" if 90 <= angulo_codo <= 120 else "❌ Ajustar codo",
            "✅ Manos sobre la frente" if manos_sobre_frente else "❌ Subir manos sobre la frente",
            "✅ Rodilla correcta" if 100 <= angulo_rodilla <= 140 else "❌ Ajustar rodilla",
            "✅ Tronco estable" if 75 <= angulo_tronco <= 105 else "❌ Ajustar tronco"
        ]
        return "\n".join(evaluacion)

    except Exception as e:
        return f"❌ Error en detección: {str(e)}"

# Cargar video
cap = cv2.VideoCapture('HowToTimeAVolleyball.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = results.pose_landmarks.landmark
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        resultados = detectar_colocador(landmarks, frame_number)

        for i, line in enumerate(resultados.split('\n')):
            cv2.putText(frame, line, (50, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if '✅' in line else (0, 0, 255), 2)

    cv2.imshow('Evaluación de Postura', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
