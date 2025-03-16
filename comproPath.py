import os
import cv2

video_path = "C:\\pryDballTrainer\\Videos\\Setter2.mp4"

if not os.path.exists(video_path):
    print(f"El archivo de video no existe: {video_path}")
else:
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: No se puede abrir el video.")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se puede recibir el frame. Saliendo...")
                break
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()