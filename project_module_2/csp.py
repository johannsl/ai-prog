# http://www.cs.mtu.edu/~nilufer/classes/cs5811/2014-fall/lecture-slides/cs5811-ch06-csp.pdf
import itertools


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.queue = []

        self.revised_total = 0

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
            , envir)

    def revise(self, assignment):

        i = assignment[0]
        j = assignment[1]
        g = self.makefunc(["x", "y"], "x != y")

        revised = False
        for x in self.domains[i]:
            for y in self.domains[j]:
                if not apply(g, (x, y)):
                    print "removing", x, "from", self.domains[i]
                    self.domains[i].remove(x)
                    if len(self.domains[i]) == 1: self.revised_total += 1
                    revised = True
        return revised

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

    def initialize(self):
        for i in self.variables:
            for j in self.constraints[i]:
                self.queue.append((i, j))

    def domain_filter_loop(self):
        while self.queue:
            current = self.queue.pop()
            print current
            if self.revise(current):
                for i in self.constraints[current[0]]:
                    if i != current[1]:
                        print "appending to queue"
                        self.queue.append((current[0], i))

    def rerun(self):
        return

    def is_solved(self):
        return True if self.revised_total == len(self.variables) else False
