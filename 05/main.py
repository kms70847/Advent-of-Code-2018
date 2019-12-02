def paired(a,b):
    return a.upper() == b.upper() and a != b

with open("input") as file:
    s = file.read().strip()

dirty = True
while dirty:
    dirty = False
    next_s = []
    i = 0
    while i < len(s):
        if i+1 < len(s) and paired(s[i], s[i+1]):
            i += 2
            dirty = True
        else:
            next_s.append(s[i])
            i += 1
    s = "".join(next_s)
print(len(s))