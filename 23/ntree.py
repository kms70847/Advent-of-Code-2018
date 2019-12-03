def iter_pairs(seq):
    for i in range(len(seq)-1):
        yield seq[i], seq[i+1]

class NRect:
    """Like Rect, but skupporting any number of dimensions"""
    def __init__(self, minbounds, maxbounds):
        assert len(minbounds) == len(maxbounds)
        self.minbounds = minbounds
        self.maxbounds = maxbounds

    @property
    def dimensions(self):
        return len(self.minbounds)

    def encompasses(self, other):
        return (
            all(a <= b for a,b in zip(self.minbounds, other.minbounds))
            and
            all(a >= b for a,b in zip(self.maxbounds, other.maxbounds))
        )

    def intersect(self, other):        
        result = {"self": [], "other": [], "both": [], "neither": []}
        borders_by_dim = []
        for i in range(self.dimensions):
            borders = sorted({self.minbounds[i], self.maxbounds[i], other.minbounds[i], other.maxbounds[i])
            #diverging from the Rect implementation a bit by storing l-r pairs rather than just fenceposts. It's more memory intensive but makes the next loop easier.
            borders_by_dim.append(list(iter_pairs(borders)))
        
        for bounds in itertools.product(*borders_by_dim):
            minbounds = [t[0] for t in bounds]
            maxbounds = [t[1] for t in bounds]
            rect = NRect(minbounds, maxbounds)
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

    def contains_point(self, coords):
        return all(a <= x < b for x,a,b in zip(coords, self.minbounds, self.maxbounds))
    
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
        return all(
            overlaps_2d((self.minbounds[i], self.maxbounds[i]), (other.minbounds[i], other.maxbounds[i]))
            for i in self.dimensions
        )

    def __repr__(self):
        return f"Rect({self.minbounds}, {self.maxbounds})"

