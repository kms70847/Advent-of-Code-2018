import collections
import copy


class State:
    OPEN = "."
    TREES = "|"
    LUMBER = "#"
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[State.OPEN]*width for _ in range(height)]
    def tick(self):
        newfield = [[None]*self.width for _ in range(self.height)]
        #newfield = copy.deepcopy(self.field)
        for i in range(self.width):
            for j in range(self.height):
                tile = self.field[j][i]
                c = self.census(i,j)
                if tile == State.OPEN and c[State.TREES] >= 3:
                    newfield[j][i] = State.TREES
                elif tile == State.TREES and c[State.LUMBER] >= 3:
                    newfield[j][i] = State.LUMBER
                elif tile == State.LUMBER and not (c[State.TREES] >= 1 and c[State.LUMBER] >= 1):
                    newfield[j][i] = State.OPEN
                else:
                    newfield[j][i] = tile
        self.field = newfield

    def census(self, x, y):
        c = collections.Counter()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0: continue
                if 0 <= x+dx < self.width and 0 <= y+dy < self.height:
                    c[self.field[y+dy][x+dx]] += 1
        return c
    def value(self):
        a = 0
        b = 0
        for row in self.field:
            for item in row:
                if item == State.TREES:
                    a += 1
                elif item == State.LUMBER:
                    b += 1
        return a*b
    def copy(self):
        return State.loads(repr(self))
    def __repr__(self):
        return "\n".join("".join(row) for row in self.field)
    def __hash__(self):
        return hash(repr(self))
    def __eq__(self, other):
        return self.field == other.field
    @staticmethod
    def load(filename):
        with open(filename) as file:
            return State.loads(file.read())
    @staticmethod
    def loads(s):
        lines = s.strip().split("\n")
        height = len(lines)
        width = len(lines[0].strip())
        x = State(width, height)
        for j in range(height):
            for i in range(width):
                x.field[j][i] = lines[j][i]
        return x        

#part 1
x = State.load("input")
for _ in range(10):
    x.tick()
print(x.value())

#part 2
x = State.load("input")
age = 0
history = {x.copy(): age}
while True:
    x.tick()
    age += 1
    if x in history:
        previous_age = history[x]
        break
    history[x.copy()] = age

target = ((1000000000-previous_age) % (age-previous_age)) + previous_age
state = next(x for x, a in history.items() if a == target)
print(state.value())
#216293: too high