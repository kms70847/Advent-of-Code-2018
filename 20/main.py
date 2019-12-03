import pprint
from geometry import Point

def parse_concat():
    global i
    values = []
    while True:
        if s[i].isalnum():
            values.append({"kind": "literal", "value": s[i]})
            i += 1
        elif s[i] == "(":
            values.append(parse_disjoint())
        else:
            break
    return {"kind": "concat", "children": values}

def parse_disjoint():
    global i
    assert s[i] == "("
    i += 1
    values = []
    while True:
        if s[i].isalnum():
            values.append(parse_concat())
        elif s[i] == "(":
            #values.append(parse_disjoint())
            values.append(parse_concat())
        elif s[i] == ")":
            break
        elif s[i] == "|":
            i += 1
            if s[i] == ")":
                values.append({"kind": "epsilon"})
                break
    assert s[i] == ")"
    i += 1
    return {"kind": "disjoint", "children": values}

#problem: parse_disjoint can't determine that (A|B)C is a concat rather than a disjoint

def generate_outputs(node):
    if node["kind"] == "concat":
        acc = [""]
        for child in node["children"]:
            rights = generate_outputs(child)
            acc = [left + right for left in acc for right in rights]
        return acc
    elif node["kind"] == "disjoint":
        acc = []
        for child in node["children"]:
            acc.extend(generate_outputs(child))
        return acc
    elif node["kind"] == "literal":
        return [node["value"]]
    elif node["kind"] == "epsilon":
        return [""]
    else:
        raise Exception(f"Not implemented yet for kind {node['kind']}")
    return outputs

def product(seq):
    x = 1
    for item in seq:
        x *= item
    return x

def output_count(node):
    if node["kind"] == "concat":
        return product(output_count(child) for child in node["children"])
    elif node["kind"] == "disjoint":
        return sum(output_count(child) for child in node["children"])
    elif node["kind"] == "literal":
        return 1
    elif node["kind"] == "epsilon":
        return 1 #?

dirs = {
    "N": Point(0,-1),
    "E": Point(1,0),
    "W": Point(-1,0),
    "S": Point(0,1)
}
class State:
    def __init__(self, seen=None, endpoints=None):
        self.seen = {Point(0,0)} if seen is None else seen
        self.endpoints = {Point(0,0)} if endpoints is None else endpoints
    def concat(self, other):
        new_seen = {endpoint+p for endpoint in self.endpoints for p in other.seen}
        new_endpoints = {a+b for a in self.endpoints for b in other.endpoints}
        return State(new_seen | self.seen, new_endpoints)
    def disjoint(self, other):
        return State(self.seen | other.seen, self.endpoints | other.endpoints)
    def copy(self):
        return State(self.seen.copy(), self.endpoints.copy())
    def show(self):
        left   = min(p.x for p in self.seen)
        right  = max(p.x for p in self.seen)
        top    = min(p.y for p in self.seen)
        bottom = max(p.y for p in self.seen)
        rows = []
        for j in range(top, bottom+1):
            row = []
            for i in range(left, right+1):
                row.append("@" if i == 0 and j==0 else "X" if Point(i,j) in self.seen else ".")
            rows.append("".join(row))
        print("\n".join(rows))
    def __repr__(self):
        return f"State({repr(self.seen)}, {repr(self.endpoints)})"
    @staticmethod
    def from_literal(s):
        return State({Point(0,0), dirs[s], dirs[s]*2}, {dirs[s]*2})

def traversed(node):
    if node["kind"] == "literal":
        return State.from_literal(node["value"])
    elif node["kind"] == "epsilon":
        return State()
    elif node["kind"] == "concat":
        x = State()
        for child in node["children"]:
            cur = traversed(child)
            x = x.concat(cur)
        return x
    elif node["kind"] == "disjoint":
        states = [traversed(child) for child in node["children"]]
        x = states[0].copy()
        for item in states[1:]:
            x = x.disjoint(item)
        return x
    else:
        raise Exception(f"Not implemented yet for kind {node['kind']}")

import sys
sys.setrecursionlimit(10**9)
with open("input") as file:
    s = file.read().strip("\n^")
i = 0
x = parse_concat()
assert s[i] == "$"
state = traversed(x)

round = 0
to_visit={Point(0,0)}
dists = {}
while to_visit:
    to_visit_next = set()
    for p in to_visit:
        dists[p] = round
        for delta in dirs.values():
            neighbor = p+delta
            if neighbor in state.seen and neighbor not in dists:
                to_visit_next.add(neighbor)
    to_visit = to_visit_next
    round += 1
#part 1
print((round-1)//2)

print(sum(1 for x in dists.values() if x%2 == 0 and x//2 >= 1000))