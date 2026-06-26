import cv2

def tomar_foto():
    # Iniciar la cámara (el 0 indica la cámara predeterminada de tu equipo)
    camara = cv2.VideoCapture(1)

    if not camara.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    print("Tomando foto...")
    
    resultado, imagen = camara.read()

    if resultado:
        nombre_archivo = "mi_foto.png"
        cv2.imwrite(nombre_archivo, imagen)
        print(f"¡Éxito! La foto se ha guardado como '{nombre_archivo}'.")
    else:
        print("Error: No se pudo capturar la imagen.")

    # IMPORTANTE: Liberar la cámara para que otros programas puedan usarla
    camara.release()

tomar_foto()
