import uuid

class Node:
    def __init__(self, g, h, f, parent, childs):
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.childs = childs

        self.domains = {}

        def __lt__(self, other):
            if self.f == other.f: return self.h < other.h
            return self.f < other.f

        def __hash__(self):
            return uuid.uuid4()
