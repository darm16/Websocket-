from fastapi import FastAPI, WebSocket
import cv2
import numpy as np
from ultralytics import YOLO
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar el directorio para servir la página HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar los modelos YOLO
ocr_model = YOLO('OCRMODEL0.947.pt')  # Ruta del modelo OCR
damage_model = YOLO('checkcontainermodel0.92.pt')  # Ruta del modelo de daños

@app.websocket("/ws")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Recibir el frame del cliente
            frame = await websocket.receive_bytes()
            nparr = np.frombuffer(frame, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Hacer las inferencias con los modelos
            ocr_results = ocr_model.predict(img)
            damage_results = damage_model.predict(img)

            # Anotar el frame con los resultados
            annotated_frame = img.copy()

            # Añadir anotaciones de OCR
            for ocr_result in ocr_results:
                for box in ocr_result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, "OCR Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Añadir anotaciones de detección de daños
            for damage_result in damage_results:
                for box in damage_result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(annotated_frame, "Damage Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Codificar el frame anotado y enviarlo de vuelta
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            print("Enviando frame con anotaciones al cliente")
            await websocket.send_bytes(buffer.tobytes())
        except Exception as e:
            print(f"Error: {e}")
            break