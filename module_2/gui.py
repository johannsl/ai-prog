##GUI is an interface subclass of Tkinter
class GUI(tk.Tk):
    def __init__(self, graph):
        tk.Tk.__init__(self)
        self.graph = graph
        self.graph_size = 800.0
        self.vertex_size = 10.0
        self.update_speed = 5

        #Create the menu
        menubar = tk.Menu(self)
        execmenu = tk.Menu(menubar)
        execmenu.add_command(label="2 Colors", command=self.execute_2)
        execmenu.add_command(label="3 Colors", command=self.execute_3)
        execmenu.add_command(label="4 Colors", command=self.execute_4)
        execmenu.add_command(label="5 Colors", command=self.execute_5)
        execmenu.add_command(label="6 Colors", command=self.execute_6)
        execmenu.add_command(label="7 Colors", command=self.execute_7)
        execmenu.add_command(label="8 Colors", command=self.execute_8)
        execmenu.add_command(label="9 Colors", command=self.execute_9)
        execmenu.add_command(label="10 Colors", command=self.execute_10)
        menubar.add_cascade(label="Colors", menu=execmenu)
        self.config(menu=menubar)

        #Create a canvas to put the graph on. Set the size of boxes
        self.canvas = tk.Canvas(self, width=self.graph_size+50, height=self.graph_size+50, borderwidth=10)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.oval = {}

        #Loop through the graph and create a two dimensional grid with circles and lines
        for edge in graph.edges:
            x1 = (graph.graph[edge[0]].pos_x * (self.graph_size / graph.x_size)) + (self.vertex_size / 2)
            x2 = (graph.graph[edge[0]].pos_y * (self.graph_size / graph.y_size)) + (self.vertex_size / 2)
            y1 = (graph.graph[edge[1]].pos_x * (self.graph_size / graph.x_size)) + (self.vertex_size / 2)
            y2 = (graph.graph[edge[1]].pos_y * (self.graph_size / graph.y_size)) + (self.vertex_size / 2)
            self.canvas.create_line(x1, x2, y1, y2)
        for vertex in graph.graph:
            x1 = vertex.pos_x * (self.graph_size / graph.x_size)
            y1 = vertex.pos_y * (self.graph_size / graph.y_size)
            x2 = x1 + self.vertex_size
            y2 = y1 + self.vertex_size
            self.oval[vertex.pos_x, vertex.pos_y] = self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill="gray80", tag="oval")
        
        #Place the window in the topmost left corner to prevent glitches in the gui
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        ###TESTINT ZONE###
        self.execute_3()

#        csp = CSP(graph)
#        print csp.domains
#        csp.initialize()
#        print csp.domains
#        csp.domain_filter_loop()
#        print csp.domains
#        if csp.is_solved():
#            print "solved!"
#            print csp.domains
#        if csp.contradictory:
#            print "no solution can be found"
#            print csp.domains
#            exit()
#        if not csp.is_solved():
#            print "not solved yet, trying astar"
#            print csp.domains
#            #astar = AStar()


#    def csp_to_graph(self, csp):
#        vertices = []
#        for v in csp.variables:
#            l = [v, 0.0, 0.0]
#            vertices.append(l)
#        graph = Graph()

    #Execute algorithm with different amount of colors... Bad style, should rewrites
    def execute_2(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(2):
            colors.append(color_list[i])
        
        ###TESTING SPACE####
        self.csp_search = CSP(graph=self.graph, domain_size=len(colors))
        #self.csp_search = csp_j.CSP(graph=self.graph, domain_size=len(colors))

        self.redraw()
        return

    def execute_3(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(3):
            colors.append(color_list[i])
        ###TESTING SPACE####
        self.csp_search = CSP(graph=self.graph, domain_size=len(colors))
        #n0 = State(self.csp_search, self.csp_search.calc_heuristic())
        #self.astar_search = AStar(graph=self.graph, n0=n0, search_type="best-first", distance_type="csp", max_nodes=1000)
        self.redraw()
        return
    
    def execute_4(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(4):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return
    
    def execute_5(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(5):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return
    
    def execute_6(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(6):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return
    
    def execute_7(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(7):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return
    
    def execute_8(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(8):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return
    
    def execute_9(self):
        self.canvas.itemconfig("oval", fill="gray80")
        colors = []
        for i in range(9):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return
    
    def execute_10(self):
        self.canvas.itemconfig("oval", fill="gray80") 
        colors = []
        for i in range(10):
            colors.append(color_list[i])
        print colors
        #self.redraw()
        return



    #Draws the gui with nodes from the open, closed, and complete path list
    def redraw(self):
        result = self.csp_search.incremental_solver()
        print self.csp_search.domains
        if (len(self.csp_search.queue)) == 0:
            if not self.csp_search.is_solved():
                print "use a star"
                self.astar_search.incremental_solver()
                exit()
        if self.csp_search.contradictory:
            print "unsolvable"
            exit()

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

        #Delay before next drawing phase
        self.after(self.update_speed, lambda: self.redraw())