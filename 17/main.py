import re
import os
from collections import defaultdict
from geometry import Point

UP = Point(0,-1)
DOWN = Point(0,1)
LEFT = Point(-1,0)
RIGHT = Point(1,0)

SAND = " "
CLAY = "#"
OOB = "x"
SPRING = "+"
DOWNWATER = "v"
STILLWATER = "~"
TRACE = "|"
def try_int(x):
    try:
        return int(x)
    except:
        return x

def get_bbox(points):
    return (
        min(p.x for p in points),
        min(p.y for p in points),
        max(p.x for p in points),
        max(p.y for p in points)
    )

def show():
    rows = []
    for j in range(top-1, bottom+2):
        row = []
        for i in range(left-1, right+2):
            row.append(field[Point(i,j)])
        rows.append("".join(row))
    print("\n".join(rows))


points = []
with open("input") as file:
    for line in file:
        m = re.match(r"(.)=(\d+), (.)=(\d+)..(\d+)", line)
        if not m:
            raise Exception(f"can't parse line {repr(line)}")
        i_axis, i, j_axis, j_min, j_max = map(try_int, m.groups())
        for j in range(j_min, j_max+1):
            args = (i,j) if i_axis == "x" else (j,i)
            points.append(Point(*args))

left, top, right, bottom = get_bbox(points)
field = defaultdict(lambda: SAND)

field[Point(500,0)] = SPRING


for p in points:
    field[p] = CLAY

to_visit = {Point(500,0)}
while to_visit:
    #todo: prioritize by reading order
    p = to_visit.pop()
    if p.y > bottom: continue
    tile = field[p]
    if tile == SPRING or tile == DOWNWATER:
        if field[p+DOWN] == TRACE or field[p+DOWN] == DOWNWATER:
            continue
        elif field[p+DOWN] == SAND:
            field[p+DOWN] = DOWNWATER
            to_visit.add(p+DOWN)
        elif field[p+DOWN] in (CLAY, STILLWATER):
            enclosed_sides = 0
            traced = set()
            for dir in (RIGHT, LEFT):
                i = 0
                while True:
                    i += 1
                    cand = p + dir*i
                    if field[cand] == CLAY:
                        enclosed_sides += 1
                        break
                    if field[cand+DOWN] not in (CLAY, STILLWATER):
                        field[cand] = DOWNWATER
                        to_visit.add(cand)
                        break
                    field[cand] = TRACE
                    traced.add(cand)
            if enclosed_sides == 2:
                for cand in traced | {p}:
                    field[cand] = STILLWATER
                    if field[cand+UP] == DOWNWATER:
                        to_visit.add(cand+UP)
        else:
            raise Exception(f"Don't know what to do when downwater is over tile of type {tile}")
    elif tile == STILLWATER or tile == SAND or tile == TRACE:
        pass
    else:
        show()
        raise Exception(f"Warning: Don't know how to handle tile type {repr(tile)} at position {p - Point(left, top)}")
        break
    rows = []
    for j in range(p.y-10, p.y+10):
        row = []
        for i in range(p.x-10, p.x+10):
            row.append(field[Point(i,j)])
        rows.append("".join(row))


#part 1
count = sum(1 for p, tile in field.items() if tile in (STILLWATER, TRACE, DOWNWATER) and top <= p.y <= bottom)
print(count)

#part 2
count = sum(1 for tile in field.values() if tile == STILLWATER)
print(count)