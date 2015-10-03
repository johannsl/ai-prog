__author__ = 'iver'
from csp import CSP
import sys
sys.path.append("..")
from project_module_1.a_star import AStar

def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA']
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

csp = create_map_coloring_csp()
csp.initialize()
for i, j in csp.constraints.iteritems():
    for x, y in j.iteritems():
        print i, j, x, y
csp.domain_filter_loop()
if not csp.is_solved():
    # do A-star
    astar = AStar(graph=None, search_type="best-first", distance_type="csp", max_nodes=1000)
    #AStar.

