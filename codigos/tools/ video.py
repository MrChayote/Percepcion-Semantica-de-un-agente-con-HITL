import cv2
from flask import Flask, Response
from ultralytics import YOLO 

app = Flask(__name__)

camara = cv2.VideoCapture(1)

print("Cargando modelo YOLO...")
modelo = YOLO('yolov8n.pt') 

ancho = int(camara.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(camara.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
salida = cv2.VideoWriter('mi_video_inteligente.avi', fourcc, 20.0, (ancho, alto))

def generar_y_grabar():
    while True:
        resultado, cuadro = camara.read()
        
        if not resultado:
            break
        resultados = modelo(cuadro, stream=True, verbose=False)
        for r in resultados:
            cuadro_anotado = r.plot()
        salida.write(cuadro_anotado)

        _, buffer = cv2.imencode('.jpg', cuadro_anotado)
        cuadro_en_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cuadro_en_bytes + b'\r\n')

@app.route('/')
def previsualizacion():
    return Response(generar_y_grabar(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("DETECCIÓN DE OBJETOS INICIADA")
    print("Abre tu navegador en: http://localhost:5000")
    print("PRESIONA Ctrl + C PARA DETENER")
    print("="*50 + "\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        camara.release()
        salida.release()
        print("\n¡Listo! El video con las detecciones se guardó como 'mi_video_inteligente.avi'.")
