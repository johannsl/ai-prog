import copy
import csp
import heapq
import Tkinter as tk
from copy import deepcopy
from operator import attrgetter
import sys
sys.path.append("..")
from module_1.a_star import AStar



# GUI is an interface subclass of Tkinter
class GUI(tk.Tk):
    def __init__(self, graph):
        tk.Tk.__init__(self)
        self.graph = graph
        self.astar = None
        self.csp = None

        # constants
        self.graph_size = 200.0
        self.vertex_size = 10.0
        self.update_speed = 5
        color_list = ("red", "medium blue", "yellow", "orange", "sea green", "brown", "purple", "pink", "cyan", "violet")  

        # Create the menu
        menubar = tk.Menu(self)
        execmenu = tk.Menu(menubar)
        execmenu.add_command(label="2 Colors", command= lambda: self.execute(2))
        execmenu.add_command(label="3 Colors", command= lambda: self.execute(3))
        execmenu.add_command(label="4 Colors", command= lambda: self.execute(4))
        execmenu.add_command(label="5 Colors", command= lambda: self.execute(5))
        execmenu.add_command(label="6 Colors", command= lambda: self.execute(6))
        execmenu.add_command(label="7 Colors", command= lambda: self.execute(7))
        execmenu.add_command(label="8 Colors", command= lambda: self.execute(8))
        execmenu.add_command(label="9 Colors", command= lambda: self.execute(9))
        execmenu.add_command(label="10 Colors", command= lambda: self.execute(10))
        menubar.add_cascade(label="Colors", menu=execmenu)
        self.config(menu=menubar)

        # Create a canvas to put the graph on. Set the size of boxes
        self.canvas = tk.Canvas(self, width=self.graph_size+50, height=self.graph_size+50, borderwidth=10)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.oval = {}

        # Loop through the graph and create a two dimensional grid with circles and lines
        for edge in graph.edges:
            x1 = (graph.vertices[edge[0]][1] * self.graph_size / graph.x_size) + (self.vertex_size / 2)
            x2 = (graph.vertices[edge[0]][2] * self.graph_size / graph.y_size) + (self.vertex_size / 2)
            y1 = (graph.vertices[edge[1]][1] * self.graph_size / graph.x_size) + (self.vertex_size / 2)
            y2 = (graph.vertices[edge[1]][2] * self.graph_size / graph.y_size) + (self.vertex_size / 2)
            self.canvas.create_line(x1, x2, y1, y2)
        print graph.vertices
        for vertex in graph.vertices:
            x1 = vertex[1] * (self.graph_size / graph.x_size)
            y1 = vertex[2] * (self.graph_size / graph.y_size)
            x2 = x1 + self.vertex_size
            y2 = y1 + self.vertex_size
            self.oval[vertex[1], vertex[2]] = self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="gray80", tag="oval")
        
        # Place the window in the topmost left corner to prevent glitches in the gui
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def makefunc(self, var_names, expression, envir=globals()):
        args = ""
        for n in var_names: args = args + "," + n
        return eval("(lambda " + args[1:] + ": " + expression + ")"
            , envir)

    def execute(self, domain_size):
        print "execute"
        self.canvas.itemconfig("oval", fill="gray80")
        self.astar = AStar(self.graph)
        self.csp = csp.CSP(self.graph)
        self.astar.distance_type = "csp"


        # Initiate csp
        domain = []
        g = self.makefunc(["x", "y"], "x != y")
        for i in range(domain_size):
            domain.append(i)
        for i in range(self.graph.nv):
            self.csp.add_variable(name=i, domain=domain)
        for vertex, other_vertex in self.graph.edges_dict.iteritems():
            for other_vertex in other_vertex:
                self.csp.add_constraint_one_way(vertex, other_vertex, g)
                self.csp.add_constraint_one_way(other_vertex, vertex, g)
        self.csp.initialize()
        #self.csp.domains[0] = [0]
        #self.csp.domains[1] = [1]
        #self.csp.singleton_domains = 2

        # Initiate astar
        self.astar.initialize(distance_type="csp")

        # Refine n0
        csp_result = self.csp.domain_filtering_loop()
        print csp_result
        if csp_result[0].startswith("ABORT"):
            return
        elif csp_result[0].startswith("SUCCESS"):
            return
        else:
            self.astar.n0.domains = copy.deepcopy(self.csp.domains) 
            self.redraw()
        return

    # Draws the gui with nodes from the open, closed, and complete path list
    def redraw(self):
            if self.csp.is_solved(): return

            # run astar
            astar_result = self.astar.incremental_solver()
            print astar_result
            if astar_result[0].startswith("SUCCESS"):
                self.csp.singleton_domains =+1
                current_csp_domains = deepcopy(self.csp.domains)
                found_better = False
                for node in self.astar.open_heap:

                    print "node domains", node.domains

                    # rerun csp and find best guess
                    self.csp.domains = node.domains
                    csp_rerun_result = self.csp.rerun()
                    print csp_rerun_result
                    if csp_rerun_result[0].startswith("ABORT"):
                        #self.csp.domains = current_csp_domains
                        #node.set_f(g=9000, h=9000)
                        self.astar.open_heap.remove(node)
                        self.astar.open_set.remove(node)
                        break
                    elif csp_rerun_result[0].startswith("SUCCESS"):
                        print "solution found"
                        return
                    else:
                        # fix node
                        #node.domains = self.csp.domains
                        found_better = True
                        print "ELSE"
                        node.set_f(g=0, h=self.astar.calculate_h(node))
                if found_better:
                    node = min(self.astar.open_heap, key=attrgetter('f'))
                    print "best f", node.f
                    self.csp.domains = node.domains
                else: self.csp.domains = current_csp_domains

                # fix open heap
                heapq.heapify(self.astar.open_heap)
                print self.astar.open_heap[0].domains

                # update graph in GUI

                #for domain in self.csp.domains:
                #    if len(domain) == 1:
                #        vertex = self.graph.vertices[domain]
                #        self.oval[vertex[1], vertex[2]]

                # Delay before next drawing phase
                self.after(self.update_speed, lambda: self.redraw())

            else: return



        #if result[0] == "HALT: unsolvable":
        #    return




#        if (len(self.csp_search.queue)) == 0:
#            if not self.csp_search.is_solved():
#                print "use a star"
#                self.astar_search.incremental_solver()
#                exit()
#        if self.csp_search.contradictory:
#            print "unsolvable"
#            exit()

#        #Check whether some error has been encountered
#        if not result[0] and not result[1] and not result[2]:
#            print result[3]
#            return
#                    
#        #Clears the last optimal path and draws the new optimal path, then returns
#        if result[3][0].startswith("SUCCESS: path"):
#            for i in result[1]:
#                column = i.pos_x
#                row = i.pos_y
#                item_id = self.oval[column, row]
#                self.canvas.itemconfig(item_id, fill="gray15")
#            for j in result[2]:
#                column = j.pos_x
#                row = j.pos_y
#                item_id = self.oval[column, row]
#                self.canvas.itemconfig(item_id, fill="green")
#            print result[3]
#            print self.search.search_type, ": Shortest path found: ", len(result[2]), "Nodes generated: ", len(result[0]) + len(result[1])
#            return
#
#        #Draws the open node list
#        for i in result[0]:
#            column = i.pos_x
#            row = i.pos_y
#            item_id = self.oval[column, row]
#            self.canvas.itemconfig(item_id, outline="black", fill="gray50")
#
#        #Draws the closed node list
#        for j in result[1]:
#            column = j.pos_x
#            row = j.pos_y
#            item_id = self.oval[column, row]
#            self.canvas.itemconfig(item_id, outline="black", fill="gray15")
#
#        #Draws the current best path
#        for k in result[2]:
#            column = k.pos_x
#            row = k.pos_y
#            item_id = self.oval[column, row]
#            self.canvas.itemconfig(item_id, outline="black", fill="yellow")


