from geometry import Point
import functools
import re
import heapq
from collections import defaultdict

Point.__lt__ = lambda self, other: self.tuple() < other.tuple()

def search(start, target, iter_neighbors):
    #heap that stores (cost, node) tuples. The cost represents the total cost of the path to get to the node from the start node.
    to_visit = []
    heapq.heappush(to_visit, (0, start))
    seen = set()
    while to_visit:
        cost, node = heapq.heappop(to_visit)
        if node in seen:
            continue
        if node == target:
            return cost
        seen.add(node)
        for edge_cost, neighbor in iter_neighbors(node):
            heapq.heappush(to_visit, (cost+edge_cost, neighbor))

directions = [Point(-1,0), Point(1,0), Point(0,-1), Point(0,1)]

NOTHING = 0
TORCH = 1
CLIMBING_GEAR = 2
allowed_equipment = {
    "rocky": {TORCH, CLIMBING_GEAR},
    "wet": {NOTHING, CLIMBING_GEAR},
    "narrow": {NOTHING, TORCH}
}

def iter_neighbors(node):
    position, equipped = node
    for delta in directions:
        p = position + delta
        if p.x < 0 or p.y < 0: continue
        t = type_(p)
        if equipped in allowed_equipment[t]:
            yield (1, (p, equipped))
    for item in (NOTHING, TORCH, CLIMBING_GEAR):
        if item != equipped and item in allowed_equipment[type_(position)]:
            yield (7, (position, item))

with open("input") as file:
    depth = int(file.readline().split()[1])
    target_x, target_y = list(map(int, re.findall(r"\d+",file.readline())))
    target = Point(target_x, target_y)

@functools.lru_cache(None)
def index(p):
    if p == Point(0,0):
        return 0
    elif p == target:
        return 0
    elif p.y == 0:
        return p.x * 16807
    elif p.x == 0:
        return p.y * 48271
    else:
        return erosion(p-Point(1,0)) * erosion(p-Point(0,1))

def erosion(p):
    return (index(p) + depth) % 20183
    
def type_(p):
    return ["rocky", "wet", "narrow"][erosion(p)%3]

def show():
    rows = []
    for j in range(target.y+6):
        row = []
        for i in range(target.x+6):
            p = Point(i,j)
            if p == Point(0,0):
                c = "M"
            elif p == target:
                c = "T"
            else:
                t = type_(Point(i,j))
                c = {"rocky": ".", "wet": "=", "narrow": "|"}[t]
            row.append(c)
        rows.append("".join(row))
    print("\n".join(rows))

#part 1
total_risk = 0
for j in range(target.y+1):
    for i in range(target.x+1):
        p = Point(i,j)
        total_risk += erosion(p)%3
print(total_risk)


#part 2
print(search(
    (Point(0,0), TORCH),
    (target, TORCH),
    iter_neighbors
))