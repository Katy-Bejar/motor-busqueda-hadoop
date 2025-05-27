import sys
import json

for line in sys.stdin:
    try:
        data = json.loads(line)
        video = data["video_file"]
        for slot in data.get("timeslots", []):
            for obj, count in slot.get("object_counts", {}).items():
                print(f"{obj}\t{video}")
    except Exception as e:
        continue
