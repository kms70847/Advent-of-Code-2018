from collections import Counter

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def mins(seq, key):
    result = [seq[0]]
    best_score = key(result[0])
    for item in seq[1:]:
        score = key(item)
        if score == best_score:
            result.append(item)
        elif score < best_score:
            result = [item]
            best_score = score
    return result

coords = []
with open("input") as file:
    for line in file:
        coords.append(tuple(map(int, line.split(", "))))

left = min(c[0] for c in coords)
right = max(c[0] for c in coords)
top = min(c[1] for c in coords)
bottom = max(c[1] for c in coords)

field = {}
counts = Counter()
for i in range(left, right+1):
    for j in range(top, bottom+1):
        claimants = mins(coords, key=lambda c: manhattan((i,j), c))
        if len(claimants) == 1:
            field[i,j] = claimants[0]
            counts[claimants[0]] += 1

#coords that own a tile on the edge have infinite area (I think)
edges = []
for i in range(left, right+1):
    for j in [top, bottom]:
        edges.append((i,j))
for i in [left, right]:
    for j in range(top, bottom):
        edges.append((i,j))
for c in edges:
    if c in field:
        counts[field[c]] = float("inf")

print(max(v for v in counts.values() if v != float("inf")))