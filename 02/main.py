from collections import Counter, defaultdict

def diff(a,b):
    return sum(1 for ac, bc in zip(a,b) if ac != bc)

def intersect(a,b):
    return "".join(ac for ac, bc in zip(a,b) if ac == bc)

with open("input") as file:
    data = [line.strip() for line in file]

#part 1
counts = defaultdict(int)
for line in data:
    c = Counter(line)
    for x in set(c.values()):
        counts[x] += 1
print(counts[2] * counts[3])

#part 2
for i in range(len(data)):
    for j in range(i+1, len(data)):
        if diff(data[i], data[j]) == 1:
            print(intersect(data[i], data[j]))
            exit(0)