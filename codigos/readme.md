├── src/
│   ├── ia-video.py                  # Script principal: Bucle HITL con YOLO-World
│   ├── ia-world.py                  # Servidor web Flask para vocabulario abierto
│   ├── train_homeobjects.py         # Script de fine-tuning (Fase 3)
│   └── tools/
│       ├── sim.py                   # Utilidad: Tester de cámaras (V4L2)
│       ├── video.py                 # Utilidad: Grabación YOLO estándar
│       └── foto.py                  # Utilidad: Captura de frames
