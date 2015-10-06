class Node:
    def __init__(self, tag, g, h, pos_x, pos_y, parent, kids, graph):
        self.tag = tag
        self.g = g
        self.h = h
        self.f = None
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.parent = parent
        self.kids = kids
        self.graph = graph

    # Generate all nodes connected to self    
    def generate_successors(self):
        successors = set()
        if self.pos_x < self.graph.columns-1:
            right = self.graph.graph[self.pos_x+1][self.pos_y]
            if right.tag is not "X":
                successors.add(right)
        if self.pos_y < self.graph.rows-1:
            below = self.graph.graph[self.pos_x][self.pos_y+1]
            if below.tag is not "X":
                successors.add(below)
        if self.pos_x > 0:
            left = self.graph.graph[self.pos_x-1][self.pos_y]
            if left.tag is not "X":
                successors.add(left)
        if self.pos_y > 0:
            above = self.graph.graph[self.pos_x][self.pos_y-1]
            if above.tag is not "X":
                successors.add(above)
        return successors

    # Set the g, h, and f values
    def set_f(self, g, h):
        self.g = g
        self.h = h
        self.f = g + h
    
    #The nodes are to be sorted after their f value, or if they are similar, their h value
    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f
