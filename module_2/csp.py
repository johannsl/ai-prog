import itertools


class CSP:
    def __init__(self, graph):
        self.graph = graph
        self.variables = []
        self.domains = {}
        self.constraints = {}
        self.queue = []
        self.contradictory = False

    def add_variable(self, name, domain):
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def add_constraint_one_way(self, i, j, filter_function):
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function 'filter_function',
        # so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def get_all_possible_pairs(self, a, b):
        return itertools.product(a, b)

    def initialize(self):
        for i in self.variables:
            for j in self.constraints[i]:
                self.queue.append((i, j))

    def domain_filtering_loop(self):
        while self.queue:
            todo_revise = self.queue.pop()
            if self.revise(todo_revise):
                for constraint in self.constraints[todo_revise[0]]:
                    if constraint is not todo_revise[1] and (todo_revise[0], constraint) not in self.queue:
                        self.queue.append((todo_revise[0], constraint))
        return ["HALT: domain filtering loop complete", self.domains]

    def revise(self, assignment):
        i = assignment[0]
        j = assignment[1]

        # Check compatibilities.
        revised = False
        for x in self.domains[i]:
            flag = False
            for y in self.domains[j]:
                if (x, y) in self.constraints[i][j]:
                    flag = True
            if flag == False:
                self.domains[i].remove(x)
                if len(self.domains[i]) == 0:
                    self.contradictory = True
                revised = True
        return revised

    def rerun(self):
        self.initialize()
        return self.domain_filtering_loop()

    def calc_heuristic(self):
        h = 0
        for i, j in self.domains.iteritems():
            h += len(j)
        return h

    def is_solved(self):
        singletons = 0
        for i, domain in self.domains.iteritems():
            if len(domain) == 1: singletons += 1
        return singletons == len(self.variables)
        #return len(self.variables) == len([x for x in self.domains if len(x[0]) == 1])
        #return True if self.singleton_domains == len(self.variables) else False

    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
                , envir)
