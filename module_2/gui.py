import Tkinter as tk
from a_star_gac import AStarGAC


# GUI is an interface subclass of Tkinter
class GUI(tk.Tk):
    def __init__(self, graph):
        tk.Tk.__init__(self)
        self.graph = graph

        # constants
        self.graph_size = 800.0
        self.vertex_size = 15.0
        self.update_speed = 1
        self.color_list = ("red", "medium blue", "yellow", "orange", "sea green", "brown", "purple", "white", "black", "violet")

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

    def execute(self, domain_size):
        self.canvas.itemconfig("oval", fill="gray80")
        self.astargac = AStarGAC(self.graph, domain_size)
        result = self.astargac.initialize()
        if result == "SOL":
            self.draw()
        self.run_agac()

    # Runs the algorithm and updates the GUI if needed
    def run_agac(self):
        result = self.astargac.increment()
        if result == "SOL":
            self.draw()
            self.print_solution()
            return
        elif result == "MOD":
            self.draw()
        elif result == "NON":
            pass

        # Delay before next drawing phase
        self.after(self.update_speed, lambda: self.run_agac())


    def draw(self):
        for domain in self.astargac.csp.domains:
            if len(self.astargac.csp.domains[domain]) == 1:
                vertex = self.graph.vertices[domain]
                item_id = self.oval[vertex[1], vertex[2]]
                self.canvas.itemconfig(item_id, fill=self.color_list[self.astargac.csp.domains[domain][0]])

    def print_solution(self):
        null_vertices = 0
        unsatisfied_constraints = 0
        for i, domain in self.astargac.csp.domains.iteritems():
            if len(domain) == 0: null_vertices += 1
            if len(domain) > 1: unsatisfied_constraints += 1
        parent = self.astargac.goal_node.parent
        parent_nodes = 0
        while parent:
            parent = parent.parent
            parent_nodes += 1

        print "Unsatisfied constraints:", unsatisfied_constraints
        print "Vertices without color:", null_vertices
        print "Nodes in the search tree:", len(self.astargac.astar.open_heap)
        print "Nodes that were expanded:", len(self.astargac.astar.closed_set)
        print "Length of path from start to goal:", parent_nodes
