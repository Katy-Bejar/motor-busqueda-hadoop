import os
import cv2
import json
from ultralytics import YOLO
from datetime import datetime
from collections import defaultdict, Counter

# === CARGAR MODELO ===
model = YOLO("yolov8x-world.pt")

# === CONFIGURACIÓN GENERAL ===
input_folder = "videos"
output_folder = "datos_generados"
os.makedirs(output_folder, exist_ok=True)

# === METADATOS POR VIDEO ===
video_metadata = {
    "1.mp4": {"camera_id": "cam_01", "location": "Entrada Principal", "priority": "alta"},
    "2.mp4": {"camera_id": "cam_02", "location": "Patio Trasero", "priority": "baja"},
    "3.mp4": {"camera_id": "cam_03", "location": "Zona de Bicicletas", "priority": "baja"},
    "4.mp4": {"camera_id": "cam_04", "location": "Puerta Lateral", "priority": "media"},
    "5.mp4": {"camera_id": "cam_05", "location": "Zona de Carga", "priority": "alta"}
}

# === PROCESAR TODOS LOS VIDEOS ===
for video_file in os.listdir(input_folder):
    if not video_file.endswith(".mp4"):
        continue

    print(f"🎥 Procesando: {video_file}")
    metadata = video_metadata.get(video_file)
    if not metadata:
        print(f"⚠️  No hay metadatos para {video_file}, se omite.")
        continue

    video_path = os.path.join(input_folder, video_file)
    date_today = datetime.now().strftime("%Y-%m-%d")

    data = {
        "camera_id": metadata["camera_id"],
        "location": metadata["location"],
        "priority": metadata["priority"],
        "video_file": video_file,
        "date": date_today,
        "timeslots": [],
        "alerts": []
    }

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    objects_by_hour = defaultdict(Counter)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        time_sec = frame_count / fps
        frame_count += 1

        # Salta frames para acelerar (1 cada 0.5 segundos)
        if frame_count % int(fps * 0.5) != 0:
            continue

        hour_slot = int(time_sec // 3600)
        hour_range = f"{hour_slot:02}:00-{hour_slot+1:02}:00"

        # === Detección ===
        results = model(frame, conf=0.3, iou=0.4)
        
        # === Mostrar frame con anotaciones ===
        annotated_frame = results[0].plot()
        cv2.imshow("Detección en Tiempo Real", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🚪 Procesamiento interrumpido por el usuario.")
            break
        
        
        for box in results[0].boxes:
            cls = int(box.cls)
            class_name = model.model.names[cls]
            objects_by_hour[hour_range][class_name] += 1

    cap.release()
    cv2.destroyAllWindows()


    for hour, counts in sorted(objects_by_hour.items()):
        data["timeslots"].append({
            "hour": hour,
            "object_counts": dict(counts)
        })

    output_name = f"{metadata['camera_id']}_{metadata['location'].replace(' ', '_').lower()}_{date_today}.json"
    output_path = os.path.join(output_folder, output_name)

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Guardado: {output_path}")
