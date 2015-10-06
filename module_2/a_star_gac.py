from a_star_csp import AStarCSP
from csp import CSP
from copy import deepcopy
import heapq
from operator import attrgetter


class AStarGAC:
    def __init__(self, graph, domain_size):
        self.graph = graph
        self.domain_size = domain_size
        self.astar = None
        self.csp = None
        self.astar = AStarCSP(self.graph)
        self.csp = CSP(self.graph)
        self.nodes_checked = set()
        self.goal_node = None

    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
                    , envir)

    # Return
    # "MOD" if we modified the domain
    # "SOL" if we solved the puzzle
    # "NON" if no change has happened
    def increment(self):
        # run astar
        if self.csp.is_solved():
            print "Solution found!"
            return "SOL"

        # From the pseudocode in the task description
        astar_result = self.astar.incremental_solver()
        if astar_result[0].startswith("SUCCESS"):
            current_csp_domains = deepcopy(self.csp.domains)
            found_better = False

            for node in self.astar.open_heap:
                if node not in self.nodes_checked: self.nodes_checked.add(node)
                else: continue
                self.csp.contradictory = False
                # rerun csp and find best guess
                self.csp.domains = node.domains
                csp_rerun_result = self.csp.rerun()
                if self.csp.is_solved():
                    print "Solution found"
                    self.goal_node = node
                    return "SOL"
                if self.csp.contradictory:
                    self.astar.open_heap.remove(node)
                    self.astar.open_set.remove(node)
                    continue
                else:
                    # fix node
                    node.domains = deepcopy(self.csp.domains)
                    found_better = True
                    node.set_f(g=0, h=self.astar.calculate_h(node))
            if found_better:
                node = min(self.astar.open_heap, key=attrgetter('f'))
                #node = self.astar.open_heap[0]
                #print "best f", node.f
                self.csp.domains = node.domains
                self.goal_node = node
                return "MOD"
            else:
                self.csp.domains = current_csp_domains

            heapq.heapify(self.astar.open_heap)
            return "NON"

        else: return "NON"
