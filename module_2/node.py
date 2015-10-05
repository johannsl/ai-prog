import uuid
from copy import deepcopy
from random import choice


class Node:
    def __init__(self, g, h, parent, kids):
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.kids = kids

        self.domains = {}

    def generate_successors(self):
        print "\ngenerate_successors:"
        successors = []
        helper = [(key, len(self.domains[key])) for key in self.domains.keys()]
        helper.sort(key=lambda x: x[1])
        #helper.reverse()

        #for h in helper:
        #    print "H", h
        #    print "H1", h[1]
        #    if h[1] == 1:
        #        print "removed", h
        #        helper.remove(h)
        helper = [x for x in helper if x[1] != 1]
        print "HELPER", helper
        if len(helper) == 0: return []
        current_domain = helper[0][0]
        #current_domain = choice(helper)[0]
        for domain in self.domains[current_domain]:
            successor = Node(g=0,
                     h=self.h - (len(self.domains[current_domain]) - 1),
                     parent=self,
                     kids=[])
            successor.domains = deepcopy(self.domains)
            successor.domains[helper[0][0]] = [domain]
            successors.append(successor)
        print "successors: ", successors, "\n"
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
