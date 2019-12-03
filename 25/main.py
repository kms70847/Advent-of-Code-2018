import re
import collections

def try_int(x):
    try:
        return int(x)
    except:
        return x

try_ints = lambda seq: [try_int(x) for x in seq]

def dist(a,b):
    return sum(abs(d-c) for c,d in zip(a,b))

def iter_ordered_pairs(seq):
    for i in range(len(seq)):
        for j in range(i+1, len(seq)):
            yield seq[i], seq[j]

def get_constellation(node, neighbors):
    seen = set()
    to_visit = {node}
    while to_visit:
        node = to_visit.pop()
        if node in seen: continue
        seen.add(node)
        for neighbor in neighbors[node]:
            to_visit.add(neighbor)
    return seen

points = []
with open("input") as file:
    for line in file:
        point = tuple(try_ints(re.findall(r"-?\d+", line)))
        points.append(point)

neighbors = collections.defaultdict(list)

for a,b in iter_ordered_pairs(points):
    if dist(a,b) <= 3:
        neighbors[a].append(b)
        neighbors[b].append(a)


constellations = []
to_search = set(points)
while to_search:
    node = to_search.pop()
    constellation = get_constellation(node, neighbors)
    constellations.append(constellation)
    for node in constellation:
        to_search.discard(node)
print(len(constellations))