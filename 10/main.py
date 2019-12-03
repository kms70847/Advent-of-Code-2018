import re
from geometry import Point

def state_at_time(t):
    return {star["pos"] + star["delta"]*t for star in stars}

def bbox(state):
    left   = min(p.x for p in state)
    right  = max(p.x for p in state)
    top    = min(p.y for p in state)
    bottom = max(p.y for p in state)
    return (left, top, right, bottom)

def area(state):
    left, top, right, bottom = bbox(state)
    return (right-left) * (bottom-top)

def show(state):
    if area(state) > 10000:
        raise ValueError("Can't display large states")
    left, top, right, bottom = bbox(state)
    rows = []
    for j in range(top, bottom+1):
        row = []
        for i in range(left, right+1):
            p = Point(i,j)
            row.append("*" if p in state else " ")
        rows.append("".join(row))
    print("\n".join(rows))

stars = []
with open("input") as file:
    for line in file:
        x,y,dx,dy = map(int, re.findall("-?\d+", line))
        stars.append({"pos": Point(x,y), "delta": Point(dx,dy)})


#do bisection to find the state with the approximately smallest area
left = 0
right = 100_000
epsilon = 0.01
f = lambda t: area(state_at_time(t))
while right-left > 1:
    mid = (left+right) // 2
    slope = (f(mid+epsilon) - f(mid-epsilon)) / epsilon
    if slope < 0:
        left = mid
    else:
        right = mid

#give user interactive control so they can search for a state that looks like letters
t = left
while True:
    show(state_at_time(t))
    print(f"Time={t}")
    x = input("(A)dvance, (R)ewind, (Q)uit? ").upper()
    if x == "A":
        t += 1
    elif x == "R":
        t -= 1
    elif x == "Q":
        break