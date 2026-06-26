# Directorio de Código Fuente (`copdigos/`)

Este directorio contiene la lógica de negocio, los scripts de inferencia interactiva y las utilidades del **Sistema de Percepción Semántica Adaptativa asistido por Humanos (HITL)**. Los archivos están organizados para separar el núcleo de la aplicación de las herramientas de diagnóstico local.

## Estructura de Archivos

```text
codigos/
├── ia-video.py                  # Script principal: Bucle interactivo HITL
├── ia-world.py                  # Servidor Flask para streaming Zero-Shot en tiempo real
├── train_homeobjects.py         # Script de entrenamiento offline especializado (Fase 3)
└── tools/                       # Utilidades secundarias y diagnóstico de hardware
    ├── sim.py                   # Escáner y selector de índices de cámara (V4L2)
    ├── video.py                 # Grabador y detector estándar con YOLOv8 (COCO)
    └── foto.py                  # Capturador rápido de frames individuales
