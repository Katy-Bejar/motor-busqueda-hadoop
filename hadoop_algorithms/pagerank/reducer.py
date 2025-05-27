import sys

damping = 0.85
links_map = {}
ranks = {}

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue
    node, value = parts

    if value.startswith("LINKS|"):
        links_map[node] = value.replace("LINKS|", "")
    else:
        ranks[node] = ranks.get(node, 0) + float(value)

for node in set(ranks) | set(links_map):
    new_rank = (1 - damping) + damping * ranks.get(node, 0)
    links = links_map.get(node, "")
    print(f"{node}\t{new_rank}|{links}")
