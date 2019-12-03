import re
import collections

VERBOSE = False

def try_int(x):
    try:
        return int(x)
    except:
        return x

try_ints = lambda seq: [try_int(x) for x in seq]

#like `max`, except it returns all maximum items in case of a tie.
#can also return an empty list, if seq is empty.
def maxes(seq, key=lambda x: x):
    if not seq: return []
    best = [seq[0]]
    best_score = key(seq[0])
    for item in seq[1:]:
        score = key(item)
        if score == best_score:
            best.append(item)
        elif score > best_score:
            best_score = score
            best = [item]
    return best

class Attack:
    def __init__(self, damage, kind):
        self.damage = damage
        self.kind = kind

class Group:
    def __init__(self, units, hp, weaknesses, immunities, attack, initiative, side=None, num=None):
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack = attack
        self.initiative = initiative
        self.side = side
        self.num = num

    repr_pattern = re.compile(r"(\d+) units each with (\d+) hit points( \(.*?\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)")
    @staticmethod
    def loads(s):
        m = Group.repr_pattern.match(s)
        if not m: raise Exception(f"Can't match line {repr(s)}")
        units, hp, raw_weakness, damage, kind, initiative = try_ints(m.groups())

        wims = {"weak": [], "immune": []} #aka "weanesses/immunities"
        if raw_weakness is not None:
            for clause in raw_weakness.strip("() ").split("; "):
                wim, raw_kinds = clause.split(" to ")
                wims[wim] = raw_kinds.split(", ")

        attack = Attack(damage, kind)
        return Group(units, hp, wims["weak"], wims["immune"], attack, initiative)

    @property
    def effective_power(self):
        return self.units * self.attack.damage

    @property
    def alive(self):
        return self.units > 0

    def calc_damage(self, defender):
        multiplier = 1
        if self.attack.kind in defender.weaknesses:
            multiplier = 2
        elif self.attack.kind in defender.immunities:
            multiplier = 0
        return self.effective_power * multiplier

    def deal_damage(self, defender):
        units_lost = self.calc_damage(defender) // defender.hp
        if units_lost > defender.units:
            units_lost = defender.units
        defender.units -= units_lost
        return units_lost

    def __repr__(self):
        return f"<group {self.side:13} #{self.num}>"
        wim_clauses = []
        if self.immunities:
            wim_clauses.append(f"immune to {', '.join(self.immunities)}")
        if self.weaknesses:
            wim_clauses.append(f"weak to {', '.join(self.weaknesses)}")
        wim = "(" + "; ".join(wim_clauses) + ") " if wim_clauses else ""
        return f"{self.units} units each with {self.hp} hit points {wim}with an attack that does {self.attack.damage} {self.attack.kind} damage at initiative {self.initiative}"

class DeadlockException(Exception):
    pass

class State:
    def __init__(self, groups):
        self.groups = groups
    def tick(self):
        if VERBOSE: print("tick")
        #target selection
        self.groups.sort(key=lambda g: (-g.effective_power, -g.initiative))

        targets = {}
        taken = set()
        for g in self.groups:
            candidates = [x for x in self.groups if g.side != x.side and x not in taken]
            candidates = maxes(candidates, key=lambda x: g.calc_damage(x))
            if candidates:
                target = max(candidates, key=lambda x: (x.effective_power, x.initiative))
                if g.calc_damage(target) > 0:
                    targets[g] = target
                    taken.add(target)
                    #print(f"{g} targets {target}")

        if not targets:
            raise Exception("Standoff")

        #attacking
        deadlock = True
        self.groups.sort(key=lambda g: -g.initiative)
        for g in self.groups:
            if g.alive and g in targets:
                t = targets[g]
                x = g.deal_damage(t)
                if x > 0: deadlock = False
                if VERBOSE: print(f"{g} attacks {t} for {g.calc_damage(t)} damage, killing {x} units")
        
        if deadlock: raise DeadlockException()
        self.groups = [g for g in self.groups if g.alive]

    @property
    def done(self):
        c = collections.Counter(g.side for g in self.groups)
        return len(c) == 1

    @staticmethod
    def load(filename, boost=0):
        groups = []
        cur_side = None
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if not line: continue
                elif line.endswith(":"):
                    cur_side = line.strip(":")
                    num = 1
                else:
                    g = Group.loads(line)
                    g.side = cur_side
                    if g.side == "Immune System":
                        g.attack.damage += boost
                    g.num = num
                    num += 1
                    groups.append(g)

        state = State(groups)
        return state


def result(state):
    while not state.done:
        try:
            state.tick()
        except DeadlockException: #give ties to Infection
            return "?", "Infection"
    x = sum(g.units for g in state.groups)
    return (x, state.groups[0].side)
    
filename = "input"
#part 1
state = State.load(filename)
print(result(state)[0])


left = 0
right = 100000
while right - left > 1:
    mid = (left+right)//2
    amt, side = result(State.load(filename, mid))
    if side == "Infection":
        left = mid
    else:
        right = mid

print(result(State.load(filename, right))[0])