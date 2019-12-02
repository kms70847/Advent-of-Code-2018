def paired(a,b):
    return a.upper() == b.upper() and a != b

def removed(s, c):
    return s.replace(c.lower(), "").replace(c.upper(), "")

with open("input") as file:
    s = file.read().strip()

def react(s):
    s = list(s)
    i = 0
    while i < len(s)-1:
        if paired(s[i], s[i+1]):
            del s[i:i+2]
            if i > 0:
                i -= 1
        else:
            i += 1
    return len(s)

#part 1
print(react(s))

#part 2
print(min(react(removed(s,c)) for c in set(s.lower())))