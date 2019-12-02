import re
from collections import Counter


data = []
with open("input") as file:
    for line in file:
        data.append(list(map(int, re.findall(r"\d+", line))))

counts = Counter()
for idx, left, top, width, height in data:
    for i in range(left, left+width):
        for j in range(top, top+height):
            counts[(i,j)] += 1

#part 1
print(sum(1 for v in counts.values() if v >= 2))

#part 2
for idx, left, top, width, height in data:
    if all(counts[i,j] == 1 for i in range(left, left+width) for j in range(top, top+height)):
        print(idx)
        break