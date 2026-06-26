import cv2
from flask import Flask, Response
from ultralytics import YOLO  # Importamos YOLO

app = Flask(__name__)

# Configuración de la cámara
camara = cv2.VideoCapture(1)

# Cargar el modelo YOLO (La primera vez que lo ejecutes, descargará un archivo pequeño automáticamente)
print("Cargando modelo YOLO...")
modelo = YOLO('yolov8n.pt') 

# Configuración del archivo de video
ancho = int(camara.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(camara.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
salida = cv2.VideoWriter('mi_video_inteligente.avi', fourcc, 20.0, (ancho, alto))

def generar_y_grabar():
    while True:
        resultado, cuadro = camara.read()
        
        if not resultado:
            break
            
        # ==========================================
        # 🧠 LA MAGIA DE YOLO OCURRE AQUÍ
        # ==========================================
        # Pasamos el cuadro por el modelo para detectar objetos (stream=True lo hace más rápido)
        resultados = modelo(cuadro, stream=True, verbose=False)
        
        # YOLO nos devuelve los resultados. Usamos .plot() para que dibuje 
        # automáticamente las cajas y los nombres de los objetos sobre la imagen.
        for r in resultados:
            cuadro_anotado = r.plot()
        # ==========================================

        # 1. Grabar el cuadro (ya con las cajas dibujadas) en el archivo .avi
        salida.write(cuadro_anotado)

        # 2. Enviar el cuadro anotado a la página web
        _, buffer = cv2.imencode('.jpg', cuadro_anotado)
        cuadro_en_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cuadro_en_bytes + b'\r\n')

@app.route('/')
def previsualizacion():
    return Response(generar_y_grabar(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎥 DETECCIÓN DE OBJETOS INICIADA")
    print("Abre tu navegador en: 👉 http://localhost:5000")
    print("PRESIONA Ctrl + C PARA DETENER")
    print("="*50 + "\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        camara.release()
        salida.release()
        print("\n¡Listo! El video con las detecciones se guardó como 'mi_video_inteligente.avi'.")