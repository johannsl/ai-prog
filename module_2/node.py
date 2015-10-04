class Node:
    def __init__(self, g, h, f, parent, childs):
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.childs = childs

        self.domains = {}
