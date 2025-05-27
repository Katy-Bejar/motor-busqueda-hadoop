from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app) 
index_file = "api/data/inverted_index.txt"
json_folder = "video_processor/datos_generados"

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    if not q:
        return jsonify({"error": "Falta parámetro q"}), 400

    videos = []
    with open(index_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            obj, vids = line.strip().split('\t')
            if obj.lower() == q:
                videos = vids.split(',')
                break

    results = []
    for v in videos:
        try:
            with open(os.path.join(json_folder, v + ".json"), 'r', encoding='utf-8') as jf:

                data = json.load(jf)
                results.append({
                    "camera_id": data["camera_id"],
                    "location": data["location"],
                    "date": data["date"],
                    "video_file": data["video_file"]
                })
        except:
            pass

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000)
