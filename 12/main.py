import copy

"""state is represented as a (left, s) tuple, where `left` indicates the number of the leftmost pot, and s is a string representing the state of each pot."""

def tick(state, rules):
    left, s = state
    s = "....." + s + "....."
    left -= 3
    result = []
    for i in range(2, len(s)-2):
        segment = s[i-2:i+3]
        result.append(rules.get(segment, "."))
    s = "".join(result)
    while s.startswith("."):
        s = s[1:]
        left += 1
    return left, s.rstrip(".")

def value(state):
    left, s = state
    return sum(left+idx for idx, c in enumerate(s) if c == "#")

rules = {}
with open("input") as file:
    start_state = (0, file.readline().split(": ")[1].strip())
    for line in file:
        if not line.strip(): continue
        k, v = line.strip().split(" => ")
        rules[k] = v

#part 1
state = copy.deepcopy(start_state)
for _ in range(20):
    state = tick(state, rules)
print(value(state))

#part 2
"""
After observing state for a couple dozen generations,
it's apparent that the state eventually becomes stable,
where every plant simply shifts a constant number of spaces to the left.
Once we hit this point, we can find any future state in O(1) time just by adding to `left`.
"""

gen = 0
state = copy.deepcopy(start_state)
prev_state = (0, "")
while prev_state[1] != state[1]:
    prev_state = state
    state = tick(state, rules)
    gen +=1

target = 50000000000
left_delta = state[0] - prev_state[0]

final_state = (state[0] + left_delta*(target-gen), state[1])
print(value(final_state))