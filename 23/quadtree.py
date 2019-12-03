inf = float("inf")
ninf = float("-inf")
class QuadTree:
    def __init__(self, region=None, value=0):
        if region is None:
            region = Rect(ninf, ninf, inf, inf)
        self.region = region
        self.value = value
        self.children = None
    def increment(self, region):
        if region.encompasses(self.region):
            self.value += 1
        elif self.children is not None:
            for child in self.children:
                if region.overlaps(child.region):
                    child.increment(region)
        else:
            self.children = []
            intersections = self.region.intersect(region)
            for rect in intersections["both"]:
                self.children.append(QuadTree(rect, 1))
            for rect in intersections["self"]:
                self.children.append(QuadTree(rect, 0))
    def query(self,p):
        assert self.region.contains_point(p)
        if self.children is None:
            return self.value
        else:
            for child in self.children:
                if child.region.contains_point(p):
                    return self.value + child.query(p)
        raise Exception(f"No region matches point {p}")
    def max_regions(self):
        """return a (value, regions) tuple representing the highest-valued regions in the tree"""
        if not self.children:
            return (self.value, [self.region])
        else:
            best = []
            best_score = ninf
            for child in self.children:
                score, regions = child.max_regions()
                if score == best_score:
                    best.extend(regions)
                elif score > best_score:
                    best = regions
                    best_score = score
            return self.value+best_score, best

    def __repr__(self):
        return f"<Query with region {self.region} and value {self.value} and {len(self.children or [])} childen>"

if __name__ == "__main__":
    from nrect import NRect
    
    q = QuadTree(NRect((ninf, ninf, ninf), (inf, inf, inf)))
    # q.increment(Rect(0,0,5,5))
    # q.increment(Rect(3,3,7,7))
    # q.increment(Rect(1,1,9,9))
    # q.increment(Rect(8,8,10,10))
    # q.increment(Rect(8,8,10,10))
    q.increment(NRect((0,0,0),(5,5,1)))
    q.increment(NRect((3,3,0),(7,7,1)))
    q.increment(NRect((1,1,0),(9,9,1)))
    q.increment(NRect((8,8,0),(10,10,1)))
    q.increment(NRect((8,8,0),(10,10,1)))
    rows = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(str(q.query((i,j,0))))
        rows.append("".join(row))
    print("\n".join(rows))
    print(q.max_regions())