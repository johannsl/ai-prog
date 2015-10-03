__author__ = 'iver'

def makefunc(var_names, expression, envir=globals()):
    args = ""
    for n in var_names: args = args + "," + n
    return eval("(lambda " + args[1:] + ": " + expression + ")"
                , envir)

func = makefunc(["x", "y", "z"], "x + y < 2*z")
print func(2, 3, 4)

def closure_test1():
    expr = "z * ( x + y)"
    z = 100
    return makefunc(["x", "y"], expr, locals())

print apply(closure_test1(), (3, 4))

l = [[1,2,3],[4,5,6]]

t = tuple(tuple(x) for x in l)
print hash(t)