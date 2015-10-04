from node import Node

class Graph:
    def __init__(self, nv, ne, verticies, edges):
        self.nv = nv
        self.ne = ne
        self.verticies = verticies
        self.edges = edges
        
        #grid
        self.node_list = []
        self.x_size = 0
        self.y_size = 0
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        #csp
        self.edges_dict = {}

        #ai
        self.n0 = Node(g=0, h=0, f=0, parent=None, childs=[])
        
        #Create an edge dictionary
        for vertex in verticies:
            vertex_edges = []
            for edge in edges:
                if vertex[0] == edge[0]:
                    vertex_edges.append(edge[1]) 
                elif vertex[0] == edge[1]:
                    vertex_edges.append(edge[0])
                self.edges_dict[int(vertex[0])] = vertex_edges
            
            #Find the lowest x any y values among nodes
            if vertex[1] > x_max: x_max = vertex[1]
            elif vertex[1] < x_min: x_min = vertex[1]
            if vertex[2] > y_max: y_max = vertex[2]
            elif vertex[2] < y_min: y_min = vertex[2]
        
        #Make all coordinates positive. Decide grid size
        if x_min < 0 or y_min < 0:
            self.x_size = x_max + abs(x_min)
            self.y_size = y_max + abs(y_min)
            for vertex in verticies:
                vertex[1] = vertex[1] + abs(x_min)
                vertex[2] = vertex[2] + abs(y_min)
        else:
            self.x_size = x_max
            self.y_size = y_max
       
      
      
      
      
      
      
      
      
      
      
       
        
    def goal_found(self, node):
        return False

#    #Find succeessors to a node in the graph and add them to a clockwise list
#    def generate_all_successors(self, node):
#        successors = []
#        helper = [(key, len(node.domains[key])) for key in node.domains.keys()]
#        helper.sort(key=lambda x: x[1])
#        print "lol", node.domains[helper[0][0]]
#        
#        print len(node.domains[helper[0][0]])
#
#        #for value in range(len(node.domains[helper[0]])):

        
        #successors.append()
        #for domain in node.domain:

#        if node.pos_x < self.columns-1:
#            right = self.graph[node.pos_x+1][node.pos_y]
#            if right.tag is not "X":
#                successors.append(right)
#        if node.pos_y < self.rows-1:
#            below = self.graph[node.pos_x][node.pos_y+1]
#            if below.tag is not "X":
#                successors.append(below)
#        if node.pos_x > 0:
#            left = self.graph[node.pos_x-1][node.pos_y]
#            if left.tag is not "X":
#                successors.append(left)
#        if node.pos_y > 0:
#            above = self.graph[node.pos_x][node.pos_y-1]
#            if above.tag is not "X":
#                successors.append(above)
#        return successors
#    
#    #Find the distance between a node C
#    def calculate_arc_cost(self, C, P):
#        return 1

