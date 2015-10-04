import uuid
from copy import deepcopy

class Node:
    def __init__(self, g, h, parent, kids):
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.kids = kids

        self.domains = {}

    def generate_successors(self):
        shortest_vertex = min(self.domains, key=lambda k: len(self.domains[k]))
        for domain in self.domains[shortest_vertex]:
            kid = Node(g=self.g + 1,
                     h=self.h - (len(self.domains[shortest_vertex]) - 1),
                     parent=self,
                     kids=None)
            kid.domains = deepcopy(self.domains)
            kid.domains[shortest_vertex] = [domain]
            self.kids.append(kid)
            print kid.domains
        print self.kids
        return self.kids

    def __lt__(self, other):
        if self.f == other.f: return self.h < other.h
        return self.f < other.f

    def __hash__(self):
        return uuid.uuid4().int
