__author__ = 'iver'
import sys
sys.path.append("..")
from module_1.a_star import AStar

class AStarCSP(AStar):
    def __init__(self, graph):
        AStar.__init__(self, graph)

    # This method calculates the heuristic value
    def calculate_h(self, node):
        h = 0
        for vertex, domain in node.domains.iteritems():
            h += len(domain) - 1
        return h