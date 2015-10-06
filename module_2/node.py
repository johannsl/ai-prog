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
        successors = set()
        helper = [(key, len(self.domains[key])) for key in self.domains.keys()]
        helper.sort(key=lambda x: x[1])
        helper = [x for x in helper if x[1] != 1]
        if len(helper) == 0: return []
        current_domain = helper[0][0]
        for domain in self.domains[current_domain]:
            successor = Node(g=0,
                     #h=self.h - (len(self.domains[current_domain]) - 1),
                     h=0,
                     parent=self,
                     kids=[])
            successor.domains = deepcopy(self.domains)
            successor.domains[current_domain] = [domain]
            successors.add(successor)
        return successors
    
    def set_f(self, g, h):
        self.g = g
        self.h = h
        self.f = g + h
    
    def __lt__(self, other):
        if self.f == other.f: return self.h < other.h
        return self.f < other.f

    def __hash__(self):
        return hash(str(uuid.uuid4))
