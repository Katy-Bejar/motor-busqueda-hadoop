import sys

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 2:
        continue
    node, rest = parts
    values = rest.split("|")
    rank = float(values[0])
    links = values[1].split(",") if len(values) > 1 and values[1] else []

    num_links = len(links)
    if num_links > 0:
        for link in links:
            print(f"{link}\t{rank / num_links}")
    
    print(f"{node}\tLINKS|{','.join(links)}")
