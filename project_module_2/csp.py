# http://www.cs.mtu.edu/~nilufer/classes/cs5811/2014-fall/lecture-slides/cs5811-ch06-csp.pdf

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}


    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
            , envir)

    def revise(self, csp, constraint):
        revised = False
        for i in csp.domains:
            valid = False
            g = self.makefunc(["x", "y"], constraint)
            for j in csp.constraints[i]:
                if apply(g, (i, j)):
                    valid = False
            if not valid:
                print csp.domains[i]
                print j
                csp.domains[i].remove(j)
                print "LOL: ", i
                revised = True
        return revised

    def ac3(self, csp):
        return

    def is_solved(self):
        return False
