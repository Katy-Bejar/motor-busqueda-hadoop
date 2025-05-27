import os
import json
from collections import defaultdict

input_folder = "video_processor/datos_generados"
output_file = "api/data/inverted_index.txt"
inverted_index = defaultdict(set)

for file_name in os.listdir(input_folder):
    if not file_name.endswith(".json"):
        continue
    with open(os.path.join(input_folder, file_name), 'r', encoding='utf-8') as f:
        data = json.load(f)
        video_file = data['video_file']
        for timeslot in data['timeslots']:
            for obj in timeslot['object_counts']:
                inverted_index[obj].add(video_file)

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as f:
    for obj, vids in inverted_index.items():
        f.write(f"{obj}\t{','.join(vids)}\n")

print("✅ Índice invertido generado correctamente.")
