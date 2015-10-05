from node import Node


class Graph:
    def __init__(self, nv, ne, vertices, edges):
        self.nv = nv
        self.ne = ne
        self.vertices = vertices
        self.edges = edges

        # grid
        self.node_list = []
        self.x_size = 0
        self.y_size = 0
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        # csp
        self.edges_dict = {}

        # astar
        self.n0 = Node(g=0, h=0, parent=None, kids=[])

        # Create an edge dictionary
        for vertex in vertices:
            vertex_edges = []
            for edge in edges:
                if vertex[0] == edge[0]:
                    vertex_edges.append(edge[1])
                elif vertex[0] == edge[1]:
                    vertex_edges.append(edge[0])
                self.edges_dict[int(vertex[0])] = vertex_edges

            # Find the lowest x any y values among nodes
            if vertex[1] > x_max: x_max = vertex[1]
            elif vertex[1] < x_min: x_min = vertex[1]
            if vertex[2] > y_max: y_max = vertex[2]
            elif vertex[2] < y_min: y_min = vertex[2]

        # Make all coordinates positive. Decide grid size
        if x_min < 0 or y_min < 0:
            self.x_size = x_max + abs(x_min)
            self.y_size = y_max + abs(y_min)
            for vertex in vertices:
                vertex[1] = vertex[1] + abs(x_min)
                vertex[2] = vertex[2] + abs(y_min)
        else:
            self.x_size = x_max
            self.y_size = y_max

    def goal_found(self, node):
        return False

    def start_found(self, node):
        if node == self.n0:
            return True
        return False

    # Find the distance between a node C
    def calculate_arc_cost(self, C, P):
        return 1
