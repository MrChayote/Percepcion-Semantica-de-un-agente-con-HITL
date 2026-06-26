import os
import cv2
import math
from ultralytics import YOLO

os.environ["QT_QPA_PLATFORM"] = "xcb" 

def main():
    modelo = YOLO('yolov8s-world.pt')

    clases = [
        "katana sword", 
        "toy crocodile", 
        "headphones", 
        "metal key", 
        "book", 
        "xbox controller"
    ]
    modelo.set_classes(clases)

    os.makedirs("mi_dataset/images", exist_ok=True)
    os.makedirs("mi_dataset/labels", exist_ok=True)
    contador_fotos = 0

    camara = cv2.VideoCapture(1)
    camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        exito, frame = camara.read()
        if not exito: break

        cv2.putText(frame, "Presiona 'C' para evaluar el objeto", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("Auto-Etiquetador", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord('c'):
            print("\n🔎 Evaluando...")
            resultados = modelo(frame, device=0, conf=0.10)
            cajas = resultados[0].boxes
            
            if len(cajas) == 0:
                print("No detecté absolutamente nada. Intenta otro ángulo.")
                continue

            mejor_caja = max(cajas, key=lambda x: x.conf[0])
            
            x1, y1, x2, y2 = map(int, mejor_caja.xyxy[0])
            confianza = float(mejor_caja.conf[0])
            id_clase = int(mejor_caja.cls[0])
            nombre = clases[id_clase]

            frame_pregunta = frame.copy()
            
            color = (0, 255, 0) if confianza > 0.40 else (0, 0, 255)
            
            cv2.rectangle(frame_pregunta, (x1, y1), (x2, y2), color, 3)
            texto_ia = f"Creo que es: {nombre} ({confianza*100:.0f}%)"
            cv2.putText(frame_pregunta, texto_ia, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            cv2.putText(frame_pregunta, "¿Es correcto? PRESIONA 'S' (Si) o 'N' (No)", (10, 450), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.imshow("Auto-Etiquetador", frame_pregunta)
            
            while True:
                respuesta = cv2.waitKey(0) & 0xFF
                if respuesta == ord('s'):
                    nombre_base = f"objeto_{contador_fotos:04d}"
                    ruta_img = f"mi_dataset/images/{nombre_base}.jpg"
                    ruta_txt = f"mi_dataset/labels/{nombre_base}.txt"
                    
                    cv2.imwrite(ruta_img, frame)
                    
                    h_img, w_img, _ = frame.shape
                    cx = ((x1 + x2) / 2) / w_img
                    cy = ((y1 + y2) / 2) / h_img
                    w_norm = (x2 - x1) / w_img
                    h_norm = (y2 - y1) / h_img
                    
                    with open(ruta_txt, "w") as f:
                        f.write(f"{id_clase} {cx:.6f} {cy:.6f} {w_norm:.6f} {h_norm:.6f}\n")
                        
                    print(f"¡Guardado! ({nombre_base})")
                    contador_fotos += 1
                    break
                elif respuesta == ord('n'):
                    print("Descartado. ¡Ponlo en otra posición e intenta de nuevo!")
                    break

        elif tecla == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 