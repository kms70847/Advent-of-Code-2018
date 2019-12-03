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

#coords that own a tile on the edge have infinite area (probably)
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



#part 2
field = {}
for i in range(left, right+1):
    for j in range(top, bottom+1):
        field[i,j] = sum(manhattan(coord, (i,j)) for coord in coords)

#calculate valid cells within the minimal bounding box of the coordinates
total = sum(1 for v in field.values() if v < 10000)

#walk along the edge of the bounding box. If a border cell is valid, determine how many more valid cells lie in that row or column.
for p in edges:
    if field[p] < 10000:
        total += (10000 - field[i,top]) // len(coords)

#regions diagonal to the bounding box can be calculated just from the corner value.
for p in [(left, top), (right, top), (right, bottom), (left, bottom)]:
    if field[p] < 10000:
        n = (10000 - field[i,top]) // len(coords)
        total += (n**2 + n)//2
    
print(total)