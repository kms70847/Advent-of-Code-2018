import re
from geometry import Point
from nrect import NRect

def manhattan_dist(a,b):
    return abs(a.x-b.x) + abs(a.y-b.y) + abs(a.z-b.z)

def is_between(a, left, right):
    return left <= a <= right

def intersects(a_left, a_right, b_left, b_right):
    return (
        is_between(a_left, b_left, b_right) or
        is_between(a_right, b_left, b_right) or
        is_between(b_left, a_left, a_right) or
        is_between(b_right, a_left, a_right)
    )

class Bot:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    def bounds(self):
        x,y,z = self.pos.tuple()
        r = self.radius
        return NRect(
            [x+y+z-r, x+y-z-r, x-y+z-r, x-y-z-r],
            [x+y+z+r, x+y-z+r, x-y+z+r, x-y-z+r]
        )
    def overlaps(self, other):
        return all(intersects(*(a+b)) for a,b in zip(self.bounds(), other.bounds()))
    def can_see(self, other):
        return manhattan_dist(self.pos, other.pos) <= self.radius

def get_ints(s):
    return [int(x) for x in re.findall(r"-?\d+", s)]

bots = []
with open("input") as file:
    for line in file:
        x,y,z,r = get_ints(line)
        bots.append(Bot(Point(x,y,z), r))

bot = max(bots, key=lambda b: b.radius)
print(sum(1 for b in bots if bot.can_see(b)))

from quadtree import QuadTree
q = QuadTree(NRect.make_inf(4))
for i, bot in enumerate(bots):
    print(i)
    q.increment(bot.bounds())
    
score, regions = q.max_regions()
print(f"{len(regions)} have a score of {score}")