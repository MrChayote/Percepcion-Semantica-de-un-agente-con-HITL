import cv2
from flask import Flask, Response
from ultralytics import YOLO

app = Flask(__name__)

print("Cargando la magia de YOLO-World...")
# Descargará automáticamente los pesos de la versión small (súper rápida)
modelo = YOLO('yolov8s-world.pt')

# === EL VOCABULARIO ABIERTO ===
# Le decimos exactamente qué buscar usando términos descriptivos en inglés.
# Esto reemplaza las 80 clases por defecto de COCO.
clases_personalizadas = [
    "katana sword", 
    "toy crocodile", 
    "headphones", 
    "metal key", 
    "keyworld",
    "book", 
    "xbox controller"
]
modelo.set_classes(clases_personalizadas)

# Abrir cámara (Asegúrate de que sea el índice correcto para tu webcam, probemos con 1 o 2)
camara = cv2.VideoCapture(1)

if camara.isOpened():
    # Subimos a VGA estándar para no perder objetos pequeños como la llave
    camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ancho = int(camara.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(camara.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"📷 Resolución configurada: {ancho}x{alto}")
else:
    print("❌ Error: No se pudo acceder a la cámara.")
    exit()

def generar_video_ia():
    while True:
        resultado, cuadro = camara.read()

        if not resultado:
            break

        # Detección con YOLO-World usando tu GPU
        resultados = modelo(
            cuadro,
            stream=True,
            verbose=False,
            device=0,
            conf=0.15  # Bajamos un poco la confianza porque es Zero-Shot
        )

        cuadro_anotado = cuadro

        for r in resultados:
            # plot() dibuja las cajas automáticamente con las clases que le diste
            cuadro_anotado = r.plot()

        _, buffer = cv2.imencode('.jpg', cuadro_anotado)
        cuadro_en_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            cuadro_en_bytes +
            b'\r\n'
        )

@app.route('/')
def previsualizacion():
    return Response(
        generar_video_ia(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 YOLO-WORLD: BUSCANDO OBJETOS DE LA HABITACIÓN")
    print("🌐 Abre tu navegador en: http://localhost:5000")
    print("PRESIONA Ctrl + C PARA DETENER")
    print("=" * 50 + "\n")

    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        camara.release()
        print("\n¡Cámara liberada y servidor detenido!")