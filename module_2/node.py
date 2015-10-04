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
        successors = []
        helper = [(key, len(self.domains[key])) for key in self.domains.keys()]
        helper.sort(key=lambda x: x[1])
        for h in helper:
            if h[0] == 0: helper.remove(h)
        if len(helper)  == 0: return []
        for domain in self.domains[helper[0][0]]:
            successor = Node(g=self.g + 1,
                     h=self.h - (len(self.domains[helper[0][0]]) - 1),
                     parent=self,
                     kids=None)
            successor.domains = deepcopy(self.domains)
            successor.domains[helper[0][0]] = [domain]
            successors.append(successor)
        return successors

    def __lt__(self, other):
        if self.f == other.f: return self.h < other.h
        return self.f < other.f

    def __hash__(self):
        return hash(str(uuid.uuid4))
