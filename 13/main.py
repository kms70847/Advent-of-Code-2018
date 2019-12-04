from geometry import Point

up = Point(0,-1)
down = Point(0,1)
left = Point(-1,0)
right = Point(1,0)
dir_by_glyph = {"^": up, "v": down, "<": left, ">": right}

class Cart:
    def __init__(self, pos, facing):
        self.pos = pos
        self.facing = facing
        self.crashed = False
        self.intersections_seen = 0

def tick():
    """
    move state forward by one tick.
    returns a list of crashed cart instances. May be empty.
    """
    crashes = []
    carts.sort(key = lambda cart: (cart.pos.y, cart.pos.x))
    for cart in carts:
        if cart.crashed: continue
        cart.pos += cart.facing
        for c in carts:
            if c is not cart and c.pos == cart.pos:
                assert not c.crashed, "Don't know how to handle multiple cart pileup yet"
                c.crashed = True
                cart.crashed = True
                crashes.extend([cart, c])
                break
        if track[cart.pos] == "/":
            cart.facing = {up: right, down: left, left: down, right: up}[cart.facing]
        elif track[cart.pos] == "\\":
            cart.facing = {up: left, down: right, left: up, right: down}[cart.facing]
        elif track[cart.pos] == "+":
            if cart.intersections_seen % 3 == 0: #left turn
                cart.facing = {up: left, left: down, down: right, right: up}[cart.facing]
            elif cart.intersections_seen % 3 == 2: #right turn
                cart.facing = {up: right, right: down, down: left, left: up}[cart.facing]
            #for seen % 3 == 1, go straight; no action needed
            cart.intersections_seen += 1
    carts[:] = [cart for cart in carts if not cart.crashed]
    return crashes

def load_state():
    track = {}
    carts = []
    with open("input") as file:
        for j, line in enumerate(file):
            for i, c in enumerate(line):
                if c in ">v<^":
                    carts.append(Cart(Point(i,j),dir_by_glyph[c]))
                    if c in "v^":
                        c = "|"
                    else:
                        c = "-"
                track[Point(i,j)] = c
    return track, carts


#part 1
track, carts = load_state()
while True:
    crashes = tick()
    if crashes:
        p = min(crashes, key=lambda cart: (cart.pos.y, cart.pos.x)).pos
        print(f"{p.x},{p.y}")
        break


#part 2
track, carts = load_state()
while True:
    tick()
    if len(carts) == 1:
        p = carts[0].pos
        print(f"{p.x},{p.y}")
        break