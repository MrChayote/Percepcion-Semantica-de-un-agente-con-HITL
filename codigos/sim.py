import cv2

print("Buscando cámaras disponibles...")

camaras = []
for i in range(10):  # busca hasta 10
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)  # Forzar V4L2 en Linux
    if cap.isOpened():
        print(f"✅ Cámara {i} disponible")
        camaras.append(i)
        cap.release()
    else:
        print(f"   Índice {i} no disponible")

if not camaras:
    print("❌ No se encontró ninguna cámara")
else:
    print(f"\nCámaras encontradas: {camaras}")
    indice = int(input(f"¿Qué índice quieres usar? {camaras} → "))
    
    cap = cv2.VideoCapture(indice, cv2.CAP_V4L2)
    # Ajustes recomendados
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(f'Cámara {indice} - Presiona Q para salir', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()