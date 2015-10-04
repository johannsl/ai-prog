import Tkinter as tk


# GUI is an interface subclass of Tkinter
class GUI(tk.Tk):
    def __init__(self, graph, csp, astar):
        tk.Tk.__init__(self)
        self.graph = graph
        self.csp = csp
        self.astar = astar
        self.astar.distance_type = "csp"

        # constants
        self.graph_size = 600.0
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
        for vertex in graph.vertices:
            x1 = vertex[1] * (self.graph_size / graph.x_size)
            y1 = vertex[2] * (self.graph_size / graph.y_size)
            x2 = x1 + self.vertex_size
            y2 = y1 + self.vertex_size
            self.oval[vertex[1], vertex[2]] = self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="gray80", tag="oval")
        
        # Place the window in the topmost left corner to prevent glitches in the gui
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.execute(3)

    def execute(self, domain_size):
        self.canvas.itemconfig("oval", fill="gray80")
        domain = []
        for i in range(domain_size):
            domain.append(i)
        for i in range(self.graph.nv):
            self.csp.add_variable(name=i, domain=domain)
        for vertex, other_vertex in self.graph.edges_dict.iteritems():
            for other_vertex in other_vertex:
                self.csp.add_constraint_one_way(vertex, other_vertex, lambda i, j: i != j)
                self.csp.add_constraint_one_way(other_vertex, vertex, lambda i, j: i != j)
        self.csp.initialize()
        self.astar.n0.domains = self.csp.domains
        self.astar.initialize(distance_type="csp")
        self.redraw()
        return

    # Draws the gui with nodes from the open, closed, and complete path list
    def redraw(self):
        result = self.csp.domain_filtering_loop()
        print result
        if result[0] == "HALT: dfl complete":
            print self.astar.incremental_solver()
            for node in self.astar.open_queue:
                self.csp.rerun(node)

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

        # Delay before next drawing phase
        #self.after(self.update_speed, lambda: self.redraw())
