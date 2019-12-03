from geometry import Point
from functools import lru_cache
def power(p):
    rack_id = p.x+10
    # print(rack_id)
    # print(rack_id * p.y)
    # print(rack_id * p.y + serial)
    # print((rack_id * p.y + serial) * rack_id)
    # print((((rack_id * p.y + serial) * rack_id // 100)))
    # print((((rack_id * p.y + serial) * rack_id // 100) % 10))
    return (((rack_id * p.y + serial) * rack_id // 100) % 10) - 5

def square_power(p):
    #return sum(power(p + Point(dx,dy)) for dx in range(3) for dy in range(3))
    return rect_power(p.x, p.y, p.x+3, p.y+3)

# @lru_cache(None)
# def rect_power(left, top, right, bottom):
    # """
    # find the total power of a given region of the field.
    # left and top are inclusive; right and bottom are exclusive.
    # """
    # if left == right or top == bottom:
        # #zero area rect.
        # return 0
    # elif left == right-1 and top == bottom-1:
        # return power(Point(left, top))
    # #print(" "*depth, left, top, right, bottom)
    # mid_x = (left + right) // 2
    # mid_y = (top + bottom) // 2
    # return(
        # rect_power(left, top, mid_x, mid_y) + 
        # rect_power(mid_x, top, right, mid_y) +  
        # rect_power(left, mid_y, mid_x, bottom) + 
        # rect_power(mid_x, mid_y, right, bottom)
    # )

"""
a rect is "perfect" if it's a square whose side length is a power of two, and if its left and top are both divisible by its side length.
By limiting this function to only perfect rects, we can reduce the memory footprint of the cache to manageable levels without incurring _too_ much of a performance hit.
"""
@lru_cache(None)
def perfect_rect_power(left, top, size):
    assert left % size == 0
    assert top % size == 0
    if size == 1:
        return power(Point(left, top))
    else:
        mid = size // 2
        return (
            perfect_rect_power(left,     top,     mid) +
            perfect_rect_power(left+mid, top,     mid) +
            perfect_rect_power(left,     top+mid, mid) +
            perfect_rect_power(left+mid, top+mid, mid)
        )

def subdivide_perfectly(left, top, right, bottom):
    """divide an ordinary rect into a collection of perfect rects."""
    

def rect_power(left, top, right, bottom):
    

with open("input") as file:
    serial = int(file.read())

max_size = 300

#part 1
candidates = [Point(i,j) for i in range(max_size-3) for j in range(max_size-3)]
p = max(candidates, key=square_power)
print(p, square_power(p))



best = None
best_score = float("-inf")
for size in range(1, max_size):
    for i in range(max_size-size):
        for j in range(max_size-size):
            score = rect_power(i,j,i+size, j+size)
            if score > best_score:
                best = (i, j, size)
                best_score = score
                print(best, best_score)

i,j,size = best
print(f"{i},{j},{size}")
