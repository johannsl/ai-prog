from a_star_gac import AStarGAC
from copy import deepcopy

class AStarGACCustom(AStarGAC):
    def __init__(self, graph, domain_size):
        AStarGAC.__init__(self, graph, domain_size)


    def initialize(self):
        # Initiate csp
        domain = []
        g = self.makefunc(["x", "y"], "x != y")
        for i in range(self.domain_size):
            domain.append(i)
        for i in range(self.graph.nv):
            self.csp.add_variable(name=i, domain=domain)
        for vertex, other_vertex in self.graph.edges_dict.iteritems():
            for other_vertex in other_vertex:
                self.csp.add_constraint_one_way(vertex, other_vertex, g)
                self.csp.add_constraint_one_way(other_vertex, vertex, g)

        self.csp.initialize()
        self.astar.initialize(distance_type=None)

        # Refine n0
        csp_result = self.csp.domain_filtering_loop()
        print csp_result[0]
        if self.csp.contradictory:
            print "Error in problem"
            return
        elif self.csp.is_solved():
            print "Solution found"
            return "SOL"
        else:
            self.astar.n0.domains = deepcopy(self.csp.domains)
            return "SOL"
        return