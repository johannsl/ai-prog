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

    def initialize(self):
        for i in self.variables:
            for j in self.constraints[i]:
                self.queue.append((i, j))
 
    def domain_filtering_loop(self):
        print self.constraints
        while self.queue:
            print len(self.queue)
            todo_revise = self.queue.pop()
            if self.revise(todo_revise):

                for constraint in self.constraints[todo_revise[0]]:
                    if todo_revise not in constraint:
                        self.queue.append((todo_revise[0], constraint))
                    else: print "lol"
            else: print "lol2"
        return ["HALT: dfl complete", self.domains]

    def revise(self, assignment):
            i = assignment[0]
            j = assignment[1]
            # Check compabilities.
            revised = False
            for x in self.domains[i]:
                flag = False
                for y in self.domains[j]:
                    if (x, y) in self.constraints[i][j]:
                        flag = True
                if flag == False:
                    self.domains[i].remove(x)
                    revised = True
            return revised

    def rerun(self, node):
        for i in self.constraints[node.domains[0]]:
            if i != todo_revise[1]:
                self.queue.append((todo_revise[0], i))
        return

    def calc_heuristic(self):
        h = 0
        for i, j in self.domains.iteritems():
            print i, j
            h += len(j)
        return h

    def complete_solver(self):
        return

    def is_solved(self):
        return True if self.singleton_domains == len(self.variables) else False

    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
            , envir)
