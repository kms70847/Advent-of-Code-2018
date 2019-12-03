from functools import lru_cache
def power(x,y):
    rack_id = x+10
    return (((rack_id * y + serial) * rack_id // 100) % 10) - 5

@lru_cache(None)
def square_power(left, top, size):
    if size == 0:
        return 0
    elif size == 1:
        return power(left, top)
    else:
        return (
            square_power(left, top, size-1) + 
            square_power(left+1, top+1, size-1) - 
            square_power(left+1, top+1, size-2) + 
            power(left+size-1, top) + 
            power(left, top+size-1)
        )    

with open("input") as file:
    serial = int(file.read())

max_size = 300

#part 1
candidates = [(i,j) for i in range(max_size-3) for j in range(max_size-3)]
i,j = max(candidates, key=lambda t: square_power(*t, 3))
print(f"{i},{j}")



best = None
best_score = float("-inf")
for size in range(1, max_size):
    for i in range(max_size-size):
        for j in range(max_size-size):
            score = square_power(i,j,size)
            if score > best_score:
                best = (i, j, size)
                best_score = score

i,j,size = best
print(f"{i},{j},{size}")
