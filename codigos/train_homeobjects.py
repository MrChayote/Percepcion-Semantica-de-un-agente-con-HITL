from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model.train(
    data="HomeObjects-3K.yaml",     
    epochs=100,                        
    imgsz=640,                      
    batch=16,                          
    workers=8,                         
    device=0,                          
    name="yolo11n_homeobjects_custom", 
    patience=50,                       
    optimizer="AdamW",                 
    lr0=0.01,                          
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3,
    cache=True,                        
    amp=True,                          
    exist_ok=True
)

print("El dataset quedó en: ~/datasets/homeobjects-3K")
