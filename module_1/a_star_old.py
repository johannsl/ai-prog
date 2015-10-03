#Written by johannsl 2015

#A star class
class AStar:
    def __init__(self, graph, search_type, distance_type, max_nodes):
        self.graph = graph
        self.search_type = search_type
        self.distance_type = distance_type
        self.max_nodes = max_nodes

        #Initialize the algorithm
        self.open_list = []
        self.closed_list = []
        n0 = graph.grid[graph.a_pos_x][graph.a_pos_y]
        n0.g = 0
        n0.h = self.calculate_h(n0)
        n0.f = n0.g + n0.h
        self.open_list.append(n0)

    #This method incrementally solves the problem
    def incremental_solver(self):
        
        #Check whether a path can be found        
        if not self.open_list:
            return [[], [], [], ["FAIL: no path found"]]

        #Sort the open_list according to search method, pop a node, and add it to closed_list
        if self.search_type == "best-first":
            self.open_list.sort(key=lambda x: x.f, reverse=True)
            X = self.open_list.pop()
        elif self.search_type == "breadth-first":
            X = self.open_list.pop(0)
        elif self.search_type == "depth-first":
            X = self.open_list.pop()
        else:
            return [[], [], [], ["ERROR: search_type"]]
        self.closed_list.append(X)

        #Look for end properties
        if X.tag == "B":
            path = self.retrace_path(X, [X])
            return [self.open_list, self.closed_list, path, ["SUCCESS: path found"]]

        #Generate a list of successor nodes to a node X
        successors = self.graph.generate_all_successors(X) 

        #Check whether nodes have been visited before. Update the ones that has. Add the rest to open_list
        for S in successors:
            X.kids.append(S)
            if S not in self.closed_list:
                if S not in self.open_list:
                    self.attach_and_eval(S, X)
                    self.open_list.append(S)
                elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                    self.attach_and_eval(S, X)
                    self.propagate_path_improvements(S)
            elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                self.attach_and_eval(S, X)
        
        #Return the current iteration results if the max number of generated nodes is not reached
        if len(self.open_list + self.closed_list) > self.max_nodes:
            return [[], [], [], ["ABORT: max number of nodes reached"]]
        path = self.retrace_path(X, [X])
        return [self.open_list, self.closed_list, path, ["SUCCESS: lists updated"]]

    #This method completely solves the problem
    def complete_solver(self):
        
        #Initiate agenda loop
        while self.open_list:

            #Sort the open_list according to search method, pop a node, and add it to closed_list
            if self.search_type == "best-first":
                self.open_list.sort(key=lambda x: x.f, reverse=True)
                X = self.open_list.pop()
            elif self.search_type == "breadth-first":
                X = self.open_list.pop(0)
            elif self.search_type == "depth-first":
                X = self.open_list.pop()
            else:
                return [[], ["ERROR: search_type"]]
            self.closed_list.append(X)

            #Look for end properties
            if X.tag == "B":
                path = self.retrace_path(X, [X])
                return [path, ["SUCCESS: path found"]]

            #Generate a list of successor nodes to a node X
            successors = self.graph.generate_all_successors(X) 

            #Check whether nodes have been visited before. Update the ones that has. Add the rest to open_list
            for S in successors:
                X.kids.append(S)
                if S not in self.closed_list:
                    if S not in self.open_list:
                        self.attach_and_eval(S, X)
                        self.open_list.append(S)
                    elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                        self.attach_and_eval(S, X)
                        self.propagate_path_improvements(S)
                elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                    self.attach_and_eval(S, X)
            
            #Check if the max number of generated nodes is reached
            if len(self.open_list + self.closed_list) > self.max_nodes:
                return [[], ["ABORT: max number of nodes reached"]]

        #If there are no more nodes in open_list, there is no solution        
        return [[], ["FAIL: no path found"]]
    
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
            raise NotImplementedError
    
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
                self.propagate_path_improvements(C)
                
    #This method recursively finds the path from B to A and returns it as a list
    def retrace_path(self, N, path):
        if N.tag == "A":
            return path
        else:
            path.append(N.parent)
            return self.retrace_path(N.parent, path)         
