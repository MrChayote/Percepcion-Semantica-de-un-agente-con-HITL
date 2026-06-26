# Sistema de Percepción Semántica Adaptativa asistido por Humanos (HITL) para Agentes Robóticos

![Banner de Ciencia de Datos](https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif)

Este repositorio contiene la implementación de un sistema de percepción semántica y etiquetado automático asistido por humanos (HITL) utilizando modelos de visión de vocabulario abierto (Zero-Shot). El objetivo de este proyecto es mitigar la extensa carga manual en la creación de conjuntos de datos y dotar a los agentes robóticos de capacidades adaptativas en entornos variables.

## Descripción General

La percepción semántica por sí sola no es suficiente para la manipulación robótica; es el primer paso para el cálculo de *Affordances* (posibilidades de acción). Tradicionalmente, las redes neuronales convolucionales (CNN) se limitan a clases vistas en entrenamiento. Este proyecto rompe esa barrera implementando **YOLO-World**, un modelo que integra Procesamiento de Lenguaje Natural (NLP) a través de la arquitectura CLIP, permitiendo inferir la presencia de objetos atípicos (ej. *toy crocodile*, *katana sword*) basándose únicamente en similitud semántica espacial.

### El Paradigma Human-in-the-Loop (HITL)
El sistema desplaza al operador humano del rol de "creador de datos" al de **"supervisor de decisiones"**. El modelo propone una predicción (Bounding Box + Confianza), y el humano actúa como un filtro binario (`Sí` / `No`), garantizando un dataset final con una precisión del 100% libre de falsos positivos antes del entrenamiento especializado.

## Arquitectura y Metodología

El ecosistema del agente robótico está diseñado en tres fases principales:

1. **Fase 1: Etiquetado Interactivo (Implementado en `ia-video.py`)**
   El sistema captura el entorno mediante una cámara 2D. El modelo Zero-Shot evalúa la escena bajo descripciones de texto y solicita confirmación humana para extraer las coordenadas normalizadas del objeto.

2. **Fase 2: Mapeo Espacial 3D (Teórico)**
   Utilizando una cámara de profundidad (RGB-D), las coordenadas del Bounding Box 2D se proyectan al mundo real. Matemáticamente, la proyección se define como:
   
   $$[X_c, Y_c, Z_c]^T = Z \cdot K^{-1} [u, v, 1]^T$$
   
   Donde $K$ es la matriz intrínseca de la cámara, $Z$ es la profundidad y $(u, v)$ es el centroide del objeto detectado en el plano de la imagen.

3. **Fase 3: Entrenamiento Offline Especializado (`train_homeobjects.py`)**
   El dataset curado por el humano se utiliza para hacer *fine-tuning* sobre un modelo convolucional ultraligero (ej. YOLO11 Nano). Este modelo especialista reside en la memoria del robot, ejecutando inferencias en milisegundos sin el peso computacional del modelo fundacional original.

### Diagrama de Flujo
![Arquitectura del Sistema](docs/arquitectura_fases.png)

## Instalación y Uso

**1. Clonar el repositorio e instalar dependencias:**
```bash
git clone [https://github.com/tu-usuario/hitl-semantic-perception.git](https://github.com/tu-usuario/hitl-semantic-perception.git)
cd hitl-semantic-perception
pip install -r requirements.txt
