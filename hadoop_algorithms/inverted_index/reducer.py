import sys
from collections import defaultdict

current_obj = None
videos = set()

for line in sys.stdin:
    try:
        obj, video = line.strip().split("\t")
        if current_obj and obj != current_obj:
            print(f"{current_obj}\t{','.join(sorted(videos))}")
            videos = set()
        current_obj = obj
        videos.add(video)
    except:
        continue

if current_obj:
    print(f"{current_obj}\t{','.join(sorted(videos))}")
