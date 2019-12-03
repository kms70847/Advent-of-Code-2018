def iter_pairs(seq):
    for i in range(len(seq)-1):
        yield seq[i], seq[i+1]

class Rect:
    def __init__(self, l, t, r, b):
        self.left = l
        self.right = r
        self.top = t
        self.bottom = b
    def encompasses(self, other):
        return self.left <= other.left and self.right >= other.right and self.top <= other.top and self.bottom >= other.bottom
    def intersect(self, other):
        """
        returns a tuple of four rect collections (self_only, other_only, both, neither)
        each rect is guaranteed to have a positive area.
        It is not guaranteed that the rects are as efficiently divided as possible*,
        and the rect collections have no guaranteed order.

        (*For example, the intersection of these rects:
        +---+..
        |...|..
        |.+-+-+
        |.|.|.|
        +-+-+.|
        ..|...|
        ..+---+

        could be optimally divided into 5 rects:
        +-+-+..
        |.|.|..
        |.+-+-+
        |.|.|.|
        +-+-+.|
        ..|.|.|
        ..+---+

        ... But you may get 7 instead:
        +-+-+..
        |.|.|..
        +-+-+-+
        |.|.|.|
        +-+-+-+
        ..|.|.|
        ..+---+
        )        
        """

        result = {"self": [], "other": [], "both": [], "neither": []}

        x_borders = sorted({self.left, self.right, other.left, other.right})
        y_borders = sorted({self.top, other.top, self.bottom, other.bottom})

        for l, r in iter_pairs(x_borders):
            for t, b in iter_pairs(y_borders):
                rect = Rect(l,t,r,b)
                if self.encompasses(rect):
                    if other.encompasses(rect):
                        result["both"].append(rect)
                    else:
                        result["self"].append(rect)
                else:
                    if other.encompasses(rect):
                        result["other"].append(rect)
                    else:
                        result["neither"].append(rect)
        return result
    
    def contains_point(self, x, y):
        return self.left <= x < self.right and self.top <= y < self.bottom

    def overlaps(self, other):
        def overlaps_2d(a, b):
            def between(a, l, r):
                return l <= a < r
            return (
                between(a[0], b[0], b[1]) or
                between(a[1], b[0], b[1]) or
                between(b[0], a[0], a[1]) or
                between(b[1], a[0], a[1])
            )
        return (
            overlaps_2d((self.left, self.right), (other.left, other.right)) and
            overlaps_2d((self.top, self.bottom), (other.top, other.bottom))
        )
    def __repr__(self):
        return f"Rect({self.left}, {self.right}, {self.top}, {self.bottom})"