#Written by johannsl 2015

#A star class
class AStar:
    def __init__(self, graph, search_type, distance_type):
        self.graph = graph
        self.search_type = search_type
        self.distance_type = distance_type

    #This method incrementally solves the problem
    def incremental_solver(self):
        return

    #This method completely solves the problem
    def complete_solver(self):
        
        #Initialize the algorithm
        closed_list = []
        open_list = []
        n0 = self.graph.grid[self.graph.a_pos_x][self.graph.a_pos_y]
        n0.g = 0
        n0.h = self.calculate_h(n0)
        n0.f = n0.g + n0.h
        open_list.append(n0)

        #Initiate agenda loop
        while open_list:

            #Sort the open_list according to search method, pop a node, and add it to closed_list
            if self.search_type == "best-first":
                open_list.sort(key=lambda x: x.f, reverse=True)

                X = open_list.pop()
            elif self.search_type == "breadth-first":
                X = open_list.pop(0)
            elif self.search_type == "depth-first":
                X = open_list.pop()
            else:
                return "ERROR: search_type"
            closed_list.append(X)
            #print X.pos_x, X.pos_y

            #Look for end properties
            if X.tag == "B":
                path = self.retrace_path(X, [X])
                print path
                for i in path:
                    print i.pos_x, i.pos_y
                return "SUCSESS"

            #Generate a list of successor nodes to a node X
            successors = self.graph.generate_all_successors(X) 

            #Check whether nodes have been visited before. Update the ones that has. Add the rest to open_list
            for S in successors:
                node_found = False
                X.kids.append(S)
                if S not in closed_list:
                    if S not in open_list:
                        self.attach_and_eval(S, X)
                        open_list.append(S)
                    elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                        self.attach_and_eval(S, X)
                        self.propagate_path_improvements(S)
                elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                    self.attach_and_eval(S, X)

                #for c in closed_list:
                #    if c == s:
                #        if c.f > s.f:
                #            c.parent = s.parent
                #            c.g = s.g
                #            #path_improve(s)
                #        node_found = True
                #        break
                #if node_found == True:
                #    continue
                #for o in open_list:
                #    if o == s:
                #        if o.f > s.f:
                #            o.parent = s.parent
                #            o.g = s.g
                #        node_found = True
                #if node_found == True:
                #    continue
                #
                #open_list.append(s)

        #If there are no more nodes in open_list, there is no solution        
        return "FAIL"
    
    #This method calculates the h value depending on distance_type
    def calculate_h(self, node):
        if self.distance_type == "manhattan distance":
            x_distance = abs(self.graph.b_pos_x-node.pos_x)
            y_distance = abs(self.graph.b_pos_y-node.pos_y)
            manhattan_distance = x_distance + y_distance
            return manhattan_distance
        elif self.distance_type == "euclidian distance":
            raise NotImplementedError 
        else:
            return
    
    #This method sets the parent, g, h, and f value of a node C
    def attach_and_eval(self, C, P):
        C.parent = P
        C.g = P.g + self.graph.calculate_arc_cost(P, C)
        C.h = self.calculate_h(C)
        C.f = C.g + C.h
    
    #This method recursively improves the path of all kid nodes of node P
    def propagate_path_improvements(self, P):
        for C in P.kids:
            if P.g + self.graph.calculate_arc_cost(P, C) < C.g:
                C.parent = P
                C.g = P.g + self.graph.calculate_arc_cost(P, C)
                C.f = C.g + C.h
                propagate_path_improvements(self, C)
                
    #This method recursively finds the path from B to A and returns it as a list
    def retrace_path(self, N, path):
        if N.tag == "A":
            print "lol"
            print path
            return path
        else:
            path.append(N.parent)
            return self.retrace_path(N.parent, path)
         
