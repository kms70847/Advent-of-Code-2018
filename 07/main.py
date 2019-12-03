import re
from collections import defaultdict

pattern = re.compile("Step (\w) must be finished before step (\w) can begin.")

to_visit = set()

prereqs = defaultdict(set)
with open("input") as file:
    for line in file:
        a,b = pattern.match(line).groups()
        to_visit.add(a)
        to_visit.add(b)
        prereqs[b].add(a)

done = []
while to_visit:
    candidates = [c for c in to_visit if len(prereqs[c]-set(done))==0]
    c = min(candidates)
    done.append(c)
    to_visit.remove(c)
print("".join(done))


#part 2
to_visit = set(done)
pending = set()
done = set()
seconds = 0
workers = [{"task": None, "time_spent":0} for _ in range(5)]
while to_visit or pending:
    available = [c for c in to_visit if c not in pending and prereqs[c].issubset(done)]
    available.sort()
    for worker in workers:
        if available and worker["task"] is None:
            c = available.pop(0)
            to_visit.remove(c)
            pending.add(c)
            worker["task"] = c
            worker["time_spent"] = 0

    for worker in workers:
        if worker["task"] is not None:
            c = worker["task"]
            worker["time_spent"] += 1
            if worker["time_spent"] == ord(c) - ord("A") + 61:
                pending.remove(c)
                done.add(c)
                worker["task"] = None
    seconds += 1

print(seconds)