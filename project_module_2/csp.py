# Written by johannsl and iverasp 2015
# http://www.cs.mtu.edu/~nilufer/classes/cs5811/2014-fall/lecture-slides/cs5811-ch06-csp.pdf

import itertools
#from problem_specific import Graph

class CSP:
    def __init__(self, graph, domain_size):
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []
        self.singleton_domains = 0
        self.contradictory = False
        
        #Initialize values
        states = []
        edges = {} 
        for vertex in graph.graph:
            edges[vertex.index] = vertex.edges
            states.append(vertex.index) 
        for state in states:
            self.add_variable(state, [x for x in range(domain_size)])
        for state, other_states in edges.items():
            for other_state in other_states:
                self.add_constraint_one_way(state, other_state, lambda i, j: i != j)
                self.add_constraint_one_way(other_state, state, lambda i, j: i != j)

        #Initialize the queue
        self.initialize()

        print self.variables
        print self.domains
        print self.constraints

    def add_variable(self, name, domain):
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}
    
    def add_constraint_one_way(self, i, j, filter_function):
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])
    
    def get_all_possible_pairs(self, a, b):
        return itertools.product(a, b)

    def initialize(self):
        for i in self.variables:
            for j in self.constraints[i]:
                self.queue.append((i, j))

    def incremental_solver(self):
        if self.queue:
            current = self.queue.pop()
            if self.revise(current):
                for i in self.constraints[current[0]]:
                    if i != current[1]:
                        print "appending to queue", (current[0], i)
                        self.queue.append((current[0], i))
        
    def revise(self, assignment):
        i = assignment[0]
        j = assignment[1]
        g = self.makefunc(["x", "y"], "x != y")

        revised = False
        valid = True
        for xi in self.domains[i]:
            for xj in self.domains[j]:
                if apply(g, (xi, xj)): break
                print "removing", xi, "from", self.domains[i]
                self.domains[i].remove(xi)
                if len(self.domains[i]) == 1: self.singleton_domains += 1
                if len(self.domains[i]) == 0: self.contradictory = True
                revised = True
        return revised





    def complete_solver()

    def domain_filter_loop(self):
        while self.queue:
            current = self.queue.pop()
            if self.revise(current):
                for i in self.constraints[current[0]]:
                    if i != current[1]:
                        print "appending to queue", (current[0], i)
                        self.queue.append((current[0], i))
        """
        for xi in self.domains[i]:
            for xj in self.domains[j]:
                if apply(g, (xi, xj)): break
                print "removing", xi, "from", self.constraints[i][j]
                for c in self.constraints[i][j]:
                    if c[0] == xi: self.constraints[i][j].remove(c)
                if len(self.domains[i]) == 1: self.singleton_domains += 1
                if len(self.domains[i]) == 0: self.contradictory = True
                revised = True
        return revised
        """


        """
        print assignment
        revised = False
        for i in self.constraints[assignment[0]][assignment[1]]:
            valid = False
            g = self.makefunc(["x", "y"], "x != y")
            for j in self.constraints[assignment[1]][assignment[0]]:
                print "i, j: ", i, j
                if not apply(g, (i, j)):
                    valid = False
            if not valid:
                print "domains: ", self.domains[assignment[0]]
                print "removing: ", j
                self.domains[assignment[0]].remove(j)
                revised = True
        return revised
        """





    def rerun(self):
        return

    def is_solved(self):
        return True if self.singleton_domains == len(self.variables) else False



    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
            , envir)
