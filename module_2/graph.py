#Graph class containing some problem specific help for the CSP and AStar class
class Graph:
    def __init__(self,NV, NE, verticies, edges):
        self.NV = NV
        self.NE = NE
        self.verticies = verticies
        self.edges = edges
         
        #Find the lower and upper bounds of the x and y values of the verticies. Initialize verticies in the graph list
        x_min = verticies[0][1]
        x_max = verticies[0][1]
        y_min = verticies[0][2]
        y_max = verticies[0][2]
        graph = []
        for vertex in verticies:
            vertex_edges = []
            for edge in edges:
                if vertex[0] == edge[0]:
                    vertex_edges.append(edge[1]) 
                elif vertex[0] == edge[1]:
                    vertex_edges.append(edge[0])
            graph.append(Vertex(index=vertex[0], pos_x=vertex[1], pos_y=vertex[2], edges=vertex_edges, color=None))
            if vertex[1] > x_max: x_max = vertex[1]
            elif vertex[1] < x_min: x_min = vertex[1]
            if vertex[2] > y_max: y_max = vertex[2]
            elif vertex[2] < y_min: y_min = vertex[2]
        
        #Make all x and y values positive to ease the creation of a two dimensional gui grid. Decide the total x and y sizes
        if x_min < 0 or y_min < 0:
            self.x_size = x_max + abs(x_min)
            self.y_size = y_max + abs(y_min)
            for vertex in graph:
                vertex.pos_x = vertex.pos_x + abs(x_min)
                vertex.pos_y = vertex.pos_y + abs(y_min)
        else:
            self.x_size = x_max
            self.y_size = y_max
        self.graph = graph
        
        ###TESTING ZONE####
        #for i in graph:
        #    print i, i.edges
    def goal_found(self, node):
        return False

    #Find succeessors to a node in the graph and add them to a clockwise list
    def generate_all_successors(self, node):
        successors = []
        helper = [(key, len(node.domains[key])) for key in node.domains.keys()]
        helper.sort(key=lambda x: x[1])
        print "lol", node.domains[helper[0][0]]
        
        print len(node.domains[helper[0][0]])

        #for value in range(len(node.domains[helper[0]])):

        
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

