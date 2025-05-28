from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Rutas relativas desde backend.py
index_file = os.path.join("data", "inverted_index.txt")
json_folder = os.path.join("..", "video_processor", "datos_generados")
video_folder = os.path.join("..", "video_processor", "videos")

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify({"error": "Falta parámetro q"}), 400

    matched_videos = []

    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('\t')
                if len(parts) != 2:
                    continue  # línea mal formateada
                keyword, videos_str = parts
                if keyword.strip().lower() == query:
                    matched_videos = videos_str.split(',')
                    break
    except Exception as e:
        return jsonify({"error": f"Error leyendo índice: {str(e)}"}), 500

    results = []

    for video in matched_videos:
        video = video.strip()
        video_name = os.path.basename(video)
        json_file_path = os.path.join(json_folder, video_name + ".json")
        video_file_path = os.path.join(video_folder, video_name)

        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                    results.append({
                        "video_file": video_name,
                        "camera_id": data.get("camera_id"),
                        "location": data.get("location"),
                        "date": data.get("date"),
                        "video_path": video_file_path.replace("\\", "/")  # para que funcione bien en Windows
                    })
            except Exception as e:
                print(f"Error leyendo JSON {json_file_path}: {e}")

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
