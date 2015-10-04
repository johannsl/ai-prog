import itertools


class CSP:
    def __init__(self, graph):
        self.graph = graph
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []
        self.singleton_domains = 0
        self.contradictory = False
       
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

    def domain_filtering_loop(self):
        while self.queue:
            print self.queue
            current = self.queue.pop()
            if self.revisei(':


                for i in self.constraints[current[0]]:
                    #print "i", i
                    #print "current[0]", current[0]
                    if i != current[1]:
                        #print "appending to queue", (current[0], i)
                        self.queue.append([current[0], i])
        else:
            return [["HALT: dfq stuck"], self.domains]

    def revise(self, assignment, i, j):
            """The function 'Revise' from the pseudocode in the textbook.
            'assignment' is the current partial assignment, that contains
            the lists of legal values for each undecided variable. 'i' and
            'j' specifies the arc that should be visited. If a value is
            found in variable i's domain that doesn't satisfy the constraint
            between i and j, the value should be deleted from i's list of
            legal values in 'assignment'.
            """
            # Check compabilities.
            revised = False
            for x in assignment[i]:
                flag = False
                for y in assignment[j]:
                    if (x, y) in self.constraints[i][j]:
                        flag = True
                if flag == False:
                    assignment[i].remove(x)
                    revised = True
            return revised

    def revise(self, assignment):
        i = assignment[0]
        j = assignment[1]
        g = self.makefunc(["x", "y"], "x != y")

        revised = False
        valid = True

        for xi in self.domains[i]:
            for xj in self.domains[j]:
                if apply(g, (xi, xj)): break
                #print "removing", xi, "from", self.domains[i]
                self.domains[i].remove(xi)
                if len(self.domains[i]) == 1: self.singleton_domains += 1
                if len(self.domains[i]) == 0: self.contradictory = True
                revised = True
        return revised


    def calc_heuristic(self):
        h = 0
        for i, j in self.domains.iteritems():
            print i, j
            h += len(j)
        return h


    def complete_solver(self):
        return

    def domain_filter_loop(self):
        while self.queue:
            current = self.queue.pop()
            if self.revise(current):
                for i in self.constraints[current[0]]:
                    if i is not current[1]:
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
