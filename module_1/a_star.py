import heapq


# A star class
class AStar:
    def __init__(self, graph):
        self.graph = graph
        self.n0 = graph.n0
        self.search_type = "best-first"
        self.max_nodes = 1000

    def initialize(self, distance_type):
        # Initialize the algorithm
        self.distance_type = distance_type
        self.n0.g = 0
        self.n0.h = self.calculate_h(self.n0)
        self.open_set = set()
        self.open_heap = []
        self.closed_set = set()
        self.open_set.add(self.n0)
        heapq.heappush(self.open_heap, self.n0)

    # This method incrementally solves the problem
    def incremental_solver(self):

        # Check whether a path can be found
        if not self.open_set:
            return ["FAIL: no path found", [], [], []]

        # Remove the next promising node, X, from open_heap and open_set, then add it to closed_set
        if self.search_type == "best-first":
            X = heapq.heappop(self.open_heap)
            self.open_set.remove(X)
        elif self.search_type == "breadth-first":
            X = self.open_heap.pop(0)
            self.open_set.remove(X)
        elif self.search_type == "depth-first":
            X = self.open_heap.pop()
            self.open_set.remove(X)
        else:
            return ["ERROR: search_type", [], [], []]
        self.closed_set.add(X)

        # Look for end properties
        if self.graph.goal_found(node=X):
            path = self.retrace_path(X, [X])
            return ["SUCCESS: path found", self.open_set, self.closed_set, path]

        # Generate a list of successor nodes to a node X
        successors = X.generate_successors()

        # Check whether nodes have been visited before. Update the ones that has. Add the rest to open_set and open_heap
        for S in successors:
            print S
            X.kids.append(S)
            if S not in self.closed_set:
                if S not in self.open_set:
                    self.attach_and_eval(S, X)
                    self.open_set.add(S)
                    if self.search_type == "best-first":
                        heapq.heappush(self.open_heap, S)
                    elif self.search_type == "breadth-first":
                        self.open_heap.append(S)
                    elif self.search_type == "depth-first":
                        self.open_heap.append(S)
                    else:
                        return ["ERROR: search_type", [], [], []]
                elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                    self.attach_and_eval(S, X)
                    self.propagate_path_improvements(S)
            elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                self.attach_and_eval(S, X)

        # Return the current iteration results if the max number of generated nodes is not reached
        if len(self.open_set) + len(self.closed_set) > self.max_nodes:
            return ["ABORT: max number of nodes", [], [], []]
        path = self.retrace_path(X, [X])
        return ["SUCCESS: lists updated", self.open_set, self.closed_set, path]

    # This method completely solves the problem
    def complete_solver(self):

        # Initiate agenda loop
        while self.open_set:

            # Remove the next promising node from open_heap and open_set, then add it to closed_set
            if self.search_type == "best-first":
                X = heapq.heappop(self.open_heap)
                self.open_set.remove(X)
            elif self.search_type == "breadth-first":
                X = self.open_list.pop(0)
                self.open_set.remove(X)
            elif self.search_type == "depth-first":
                X = self.open_list.pop()
                self.open_set.remove(X)
            else:
                return ["ERROR: search_type", []]
            self.closed_set.add(X)

            # Look for end properties
            if self.graph.goal_found(node=X):
                path = self.retrace_path(X, [X])
                return ["SUCCESS: path found", []]

            # Generate a list of successor nodes to a node X
            successors = self.graph.generate_all_successors(X)

            # Check whether nodes have been visited before.
            # Update the ones that has. Add the rest to open_set and open_heap
            for S in successors:
                X.kids.append(S)
                if S not in self.closed_set:
                    if S not in self.open_set:
                        self.attach_and_eval(S, X)
                        self.open_set.add(S)
                        if self.search_type == "best-first":
                            heapq.heappush(self.open_heap, S)
                        elif self.search_type == "breadth-first":
                            self.open_heap.append(S)
                        elif self.search_type == "depth-first":
                            self.open_heap.append(S)
                        else:
                            return ["ERROR: search_type", []]
                    elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                        self.attach_and_eval(S, X)
                        self.propagate_path_improvements(S)
                elif X.g + self.graph.calculate_arc_cost(X, S) < S.g:
                    self.attach_and_eval(S, X)

            # Check if the max number of generated nodes is reached
            if len(self.open_set) + len(self.closed_set) > self.max_nodes:
                return ["ABORT: max number of nodes", []]

        # If there are no more nodes in open_set, there is no solution
        return ["FAIL: no path found", []]

    # This method calculates the h value depending on distance_type
    def calculate_h(self, node):
        if self.distance_type == "manhattan distance":
            x_distance = abs(self.graph.b_pos_x-node.pos_x)
            y_distance = abs(self.graph.b_pos_y-node.pos_y)
            manhattan_distance = x_distance + y_distance
            return manhattan_distance
        elif self.distance_type == "euclidian distance":
            raise NotImplementedError
        elif self.distance_type == "csp":
            h = 0
            for vertex, domain in node.domains.iteritems():
                h += len(domain) - 1
            return h
        else:
            raise NotImplementedError

    # This method sets the parent, g, h, and f value of a node C
    def attach_and_eval(self, C, P):
        C.parent = P
        C.g = P.g + self.graph.calculate_arc_cost(P, C)
        C.h = self.calculate_h(C)
        C.f = C.g + C.h

    # This method recursively improves the path of all kid nodes of node P
    def propagate_path_improvements(self, P):
        for C in P.kids:
            if P.g + self.graph.calculate_arc_cost(P, C) < C.g:
                C.parent = P
                C.g = P.g + self.graph.calculate_arc_cost(P, C)
                C.f = C.g + C.h
                self.propagate_path_improvements(C)

    # This method recursively finds the path from B to A and returns it as a list
    def retrace_path(self, N, path):
        if self.graph.start_found(node=N):
            return path
        else:
            path.append(N.parent)
            return self.retrace_path(N.parent, path)         
