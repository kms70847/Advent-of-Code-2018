from geometry import Point
from collections import Counter
from functools import lru_cache

directions = [
    Point(0,-1),
    Point(-1,0),
    Point(1,0),
    Point(0,1)
]

EMPTY = "."
WALL = "#"
OOB = " "

class Unit:
    def __init__(self, side, position, attack_points=3):
        self.side = side
        self.pos = position
        self.attack_points = attack_points
        self.hit_points = 200

    def is_dead(self):
        return self.hit_points <= 0

    def __repr__(self):
        return f"Unit({repr(self.side)}, {self.pos}, {self.attack_points}, {self.hit_points})"

class State:
    def __init__(self, width, height, allow_rout=False):
        self.units = []
        self.field = {}
        self.width = width
        self.height = height
        #do all the elves give up after the first elf death?
        self.allow_rout = allow_rout
    def add(self, unit):
        self.units.append(unit)
        self.field[unit.pos] = unit
    def iter_field(self):
        for j in range(self.height):
            for i in range(self.width):
                p = Point(i,j)
                yield p, self.field[p]
    def iter_units(self):
        """iterate units in reading order."""
        yield from sorted(self.units, key=lambda unit: (unit.pos.y, unit.pos.x))
        #todo: make this O(len(units)), not O(size(field))
        #for p, cell in self.iter_field():
        #    if isinstance(cell, Unit):
        #        yield cell
    def iter_adjacent_enemies(self, unit):
        for p in self.neighbors(unit.pos):
            cell = self.field[p]
            if isinstance(cell, Unit) and cell.side != unit.side:
                yield cell
    def iter_targets(self, unit):
        for cand in self.iter_units():
            if cand.side != unit.side:
                yield cand
    def neighbors(self, pos):
        for delta in directions:
            cand_pos = pos + delta
            if cand_pos in self.field:
                yield cand_pos
    def range_of(self, unit):
        for cand_pos in self.neighbors(unit.pos):
            if self.field[cand_pos] == EMPTY:
                yield cand_pos
    # def reachable_by(self, destination, unit):
        # seen = set()
        # to_visit = set([unit.pos])
        # while to_visit:
            # pos = to_visit.pop()
            # seen.add(pos)
            # for neighbor in self.neighbors(pos):
                # if neighbor == destination:
                    # return True
                # if neighbor not in seen and self.field[neighbor] == EMPTY:
                    # to_visit.add(neighbor)
        # return False
    def distance_plot(self, start):
        """
        create a point:int dict indicating how many steps it takes to get from `pos` to the point.
        """

        result = {}
        to_visit = {start}
        round = 0
        while to_visit:
            next_to_visit = set()
            for pos in to_visit:
                result[pos] = round
                for neighbor in self.neighbors(pos):
                    if self.field[neighbor] == EMPTY and neighbor not in result:
                        next_to_visit.add(neighbor)
            to_visit = next_to_visit
            round += 1
        return result
    def choose_movement(self, unit):
        candidates = set()
        for target in self.iter_targets(unit):
            for pos in self.range_of(target):
                candidates.add(pos)

        candidates = sorted(candidates, key=lambda p: (p.y, p.x))
        best_choice = None
        best_cost = float("inf")
        for pos in candidates:
            plot = self.distance_plot(pos)
            for delta in directions:
                p = unit.pos+delta
                if p in plot:
                    cost = plot[p]
                    if cost < best_cost:
                        best_cost = cost
                        best_choice = p
        return best_choice


    def tick(self):
        """
        simulate one round of play.
        return the name of the winning side if the game ends before a complete turn occurs, and None otherwise
        """
        #units might move around or die halfway through the turn, so make a copy here
        units = list(self.iter_units())
        side_count = Counter(unit.side for unit in units)
        if any(s not in side_count for s in ("E", "G")):
            return next(k for k,v in side_count.items() if v != 0)
        for unit in units:
            #print(unit)
            if 0 in side_count.values():
                return next(k for k,v in side_count.items() if v != 0)

            if unit.is_dead():
                continue
            
            if not any(self.iter_adjacent_enemies(unit)):
                p = self.choose_movement(unit)
                if p is not None:
                    self.field[unit.pos] = EMPTY
                    unit.pos = p
                    self.field[unit.pos] = unit
            
            attack_target = min(self.iter_adjacent_enemies(unit), key=lambda unit: unit.hit_points, default=None)
            if attack_target:
                attack_target.hit_points -= unit.attack_points
                if attack_target.is_dead():
                    self.field[attack_target.pos] = EMPTY
                    attack_target.pos = None
                    self.units.remove(attack_target)
                    side_count[attack_target.side] -= 1
                    if attack_target.side == "E" and self.allow_rout:
                        return "G"
        return None

    def outcome(self):
        round = 0
        victor = None
        while victor is None:
            round += 1
            victor = self.tick()
            #print(round)
            #print(state)
            #print(done)
            #print([(unit, unit.hit_points) for unit in state.iter_units()])

        #this round must have been incomplete, so roll back by one
        round -= 1
        hp_total = sum(unit.hit_points for unit in self.iter_units())
        return victor, round, hp_total
        

    @staticmethod
    def load(filename, elfpower=3):
        x = State(0,0)
        with open(filename) as file:
            for j, line in enumerate(file):
                for i, c in enumerate(line.rstrip()):
                    pos = Point(i,j)
                    if c == "G":
                        x.add(Unit(c, pos))
                    elif c == "E":
                        x.add(Unit(c, pos, elfpower))
                    else:
                        x.field[pos] = c
        x.width = i+1
        x.height = j+1
        return x
    def show(self, show_turn_order=False, annotations=None):
        """
        arguments:
        show_turn_order: mark each unit with a digit indicating its turn order
        annotations: optional dict keyed by position. Overwrite the contents of the indicated cell with the given value.
        
        """
        if annotations is None:
            annotations = {}
        rows = [[" " for i in range(self.width)] for j in range(self.height)]
        for p, cell in self.iter_field():
            if isinstance(cell, Unit):
                cell = cell.side
            rows[p.y][p.x] = cell
        if show_turn_order:
            for idx, unit in enumerate(self.iter_units(), 1):
                p = unit.pos
                rows[p.y][p.x] = str(idx)
        for p, c in annotations.items():
            rows[p.y][p.x] = c
        return "\n".join("".join(rows[j][i] for i in range(self.width)) for j in range(self.height))
    def __repr__(self):
        return self.show()

@lru_cache(None)
def outcome(elfpower, allow_rout):
    #print("Evaluating outcome with power", elfpower)
    state = State.load("input", elfpower)
    state.allow_rout = allow_rout
    victor, round, hp = state.outcome()
    return victor, round*hp

#part 1
_, result = outcome(3, False)
print(result)

#part 2
l = 3
r = 200
while r != l+1:
    mid = (l+r) // 2
    victor, _ = outcome(mid, True)
    if victor == "E":
        r = mid
    else:
        l = mid

_, result = outcome(r, True)
print(result)