import a_star
import Tkinter as tk

# Global values
max_nodes = 600
update_speed = 50

# GUI is based on Tkinter
class GUI(tk.Tk):
    def __init__(self, graph, cellsize):
        tk.Tk.__init__(self)
        self.graph = graph
        self.search = None
        
        #Create the menu
        menubar = tk.Menu(self)
        execmenu = tk.Menu(menubar)
        execmenu.add_command(label="Best-first search", command=self.best_first_search)
        execmenu.add_command(label="Breadth-first search", command=self.breadth_first_search)
        execmenu.add_command(label="Depth-first search", command=self.depth_first_search)
        menubar.add_cascade(label="Exec", menu=execmenu)
        self.config(menu=menubar)

        #Create a canvas to put the graph on. Set the size of boxes
        self.cellwidth = cellsize
        self.cellheight = cellsize
        self.canvas = tk.Canvas(self, width=(graph.columns*self.cellwidth)+5, height=(graph.rows*self.cellheight)+5, borderwidth=10)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rectangle = {}
        self.oval = {}

        #Loop through the graph and paint boxes. Subtract y values from total rows to simulate the exercice graphs
        for r in range(graph.rows):
            for c in range(graph.columns):
                x1 = c * self.cellwidth
                y1 = r * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if graph.graph[c][graph.rows-r-1].tag == "O":
                    self.rectangle[c, graph.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                    self.oval[c, graph.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, outline="white", tag="oval")
                if graph.graph[c][graph.rows-r-1].tag == "X":
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
                if graph.graph[c][graph.rows-r-1].tag == "A":
                    self.rectangle[c, graph.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                    self.oval[c, graph.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, tag="oval")
                    if cellsize == 25:
                        self.canvas.create_text(x1+12, y1+12, text="A")
                if graph.graph[c][graph.rows-r-1].tag == "B":
                    self.rectangle[c, graph.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                    self.oval[c, graph.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, outline="white", tag="oval")
                    if cellsize == 25:
                        self.canvas.create_text(x1+12, y1+12, text="B")
 
        #Place the window in the topmost left corner to prevent glitches in the gui
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    #Run best-first search
    def best_first_search(self):
        self.canvas.itemconfig("oval", fill="white", outline="white")
        self.search = a_star.AStar(self.graph)
        self.search.max_nodes = max_nodes
        self.search.initialize("manhattan distance")
        self.redraw()

    #Run breadth-first search
    def breadth_first_search(self):
        self.canvas.itemconfig("oval", fill="white", outline="white")
        self.search = a_star.AStar(self.graph)
        self.search.search_type = "breadth-first"
        self.search.max_nodes = max_nodes
        self.search.initialize("manhattan distance")
        self.redraw()

    #Run depth-first search
    def depth_first_search(self):
        self.canvas.itemconfig("oval", fill="white", outline="white")
        self.search = a_star.AStar(self.graph)
        self.search.search_type = "depth-first"
        self.search.max_nodes = max_nodes
        self.search.initialize("manhattan distance")
        self.redraw()

    #Draws the gui with nodes from the open, closed, and complete path list
    def redraw(self):
        result = self.search.incremental_solver()

        #Check whether some error has been encountered
        if not result[0].startswith("SUCCESS"):
            print result[0]
            return
                    
        #Clears the last optimal path and draws the new optimal path, then returns
        if result[0].startswith("SUCCESS: path found"):
            for i in self.search.closed_set:
                column = i.pos_x
                row = i.pos_y
                item_id = self.oval[column, row]
                self.canvas.itemconfig(item_id, fill="gray15")
            for j in result[1]:
                column = j.pos_x
                row = j.pos_y
                item_id = self.oval[column, row]
                self.canvas.itemconfig(item_id, fill="green")
            print result[0]
            print self.search.search_type, ": Shortest path found: ", len(result[1]), "Nodes generated: ", len(self.search.open_set) + len(self.search.closed_set)
            return
        
        #Draws the open node list
        for i in self.search.open_heap:
            column = i.pos_x
            row = i.pos_y
            item_id = self.oval[column, row]
            self.canvas.itemconfig(item_id, outline="black", fill="gray50")

        #Draws the closed node list
        for j in self.search.closed_set:
            column = j.pos_x
            row = j.pos_y
            item_id = self.oval[column, row]
            self.canvas.itemconfig(item_id, outline="black", fill="gray15")
        
        #Draws the current best path
        for k in result[1]:
            column = k.pos_x
            row = k.pos_y
            item_id = self.oval[column, row]
            self.canvas.itemconfig(item_id, outline="black", fill="yellow")

        #Delay before next drawing phase
        self.after(update_speed, lambda: self.redraw())

