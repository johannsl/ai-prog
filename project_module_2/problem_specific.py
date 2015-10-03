#Written by johannsl and iverasp 2015
#This file contains classes, methods, and functions related to the specifications of Module #2

import sys
sys.path.append("..")
from project_module_1.a_star import AStar
from csp import CSP
import datetime
import os
import platform
import random
import re
import Tkinter as tk

#These are the global values
color_list = ("red", "medium blue", "yellow", "orange", "sea green", "brown", "purple", "pink", "cyan", "violet")


#The main function runs the basic terminal communication
def main():
    
    #Clear the screen, prepare the mainlopp, create graph_list, create graph_path
    os.system("clear")
    flag = True
    graph_path = "./graphs/"
    graph_list = os.listdir(graph_path)

    #Print welcome message including the premade graph information
    print ("Project Module #2: \n"
            "A*-GAC \n"
            "\n"
            "Premade problems are:")
    
    for i in range(len(graph_list)):
        print i, graph_list[i]
    
    print ("\n"
            "'Run 0-X' for premade problem \n"
            "'Exit' ends the script \n"
            "\n")

    #This is the mainloop - It reads input from the user and executes the commands
    while flag:

        ###TESTING SPACE###
        the_input = "Run 1"

        #the_input = raw_input(" > ")
        
        #Run a premade graph
        if the_input != "Run new" and the_input.startswith("Run"):

            #Get the correct premade graph and add its numbers to a list
            number = int(the_input[4:])
            f = open(graph_path + str(graph_list[number]), "r")
            line_list = map(int, re.findall(r'\d+', f.readline()))
            
            #Structure the input from f
            number_of_verticies = line_list[0]
            number_of_edges = line_list[1]
            verticies = []
            edges = []
            
            #Fill the verticies and edges, then close f
            for i in range(number_of_verticies):
                vertex = []
                for word in f.readline().split():
                    vertex.append(float(word))
                verticies.append(vertex)
            for j in range(number_of_edges):
                edge = map(int, re.findall(r'\d+', f.readline()))
                edges.append(edge)
            f.close()
             
            #Initialize the graph
            premade_graph = Graph(NV=number_of_verticies, NE=number_of_edges, verticies=verticies, edges=edges)
            premade_graph_gui = GUI(graph=premade_graph)
            _run_gui(premade_graph_gui)
            flag = False

        #Exit the loop
        elif the_input == "Exit":
            flag = False

 
#Private run gui function aimed at making the program run more smoothly on Mac OS
def _run_gui(graph):
    if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            graph.mainloop()
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "iTerm" to true' ''')
    else: graph.mainloop()
    return


#Graph class containing some problem specific help for the CSP and AStar class
class Graph:
    def __init__(self,NV, NE, verticies, edges):
        self.NV = NV
        self.NE = NE
        self.verticies = verticies
        self.edges = edges
         
        #Find the lower and upper bounds of the x and y values of the verticies. Initialize verticies in the graph list
        x_min = verticies[0][1]
        x_max = verticies[0][1]
        y_min = verticies[0][2]
        y_max = verticies[0][2]
        graph = []
        for vertex in verticies:
            vertex_edges = []
            for edge in edges:
                if vertex[0] == edge[0]:
                    vertex_edges.append(edge[1]) 
                elif vertex[0] == edge[1]:
                    vertex_edges.append(edge[0])
            graph.append(Vertex(index=vertex[0], pos_x=vertex[1], pos_y=vertex[2], edges=vertex_edges, color=None))
            if vertex[1] > x_max: x_max = vertex[1]
            elif vertex[1] < x_min: x_min = vertex[1]
            if vertex[2] > y_max: y_max = vertex[2]
            elif vertex[2] < y_min: y_min = vertex[2]
        
        #Make all x and y values positive to ease the creation of a two dimensional gui grid. Decide the total x and y sizes
        if x_min < 0 or y_min < 0:
            self.x_size = x_max + abs(x_min)
            self.y_size = y_max + abs(y_min)
            for vertex in graph:
                vertex.pos_x = vertex.pos_x + abs(x_min)
                vertex.pos_y = vertex.pos_y + abs(y_min)
        else:
            self.x_size = x_max
            self.y_size = y_max
        self.graph = graph
        
        ###TESTING ZONE####
        #for i in graph:
        #    print i, i.edges
        
#    #Find succeessors to a node in the graph and add them to a clockwise list
#    def generate_all_successors(self, node):
#        successors = []
#        if node.pos_x < self.columns-1:
#            right = self.graph[node.pos_x+1][node.pos_y]
#            if right.tag is not "X":
#                successors.append(right)
#        if node.pos_y < self.rows-1:
#            below = self.graph[node.pos_x][node.pos_y+1]
#            if below.tag is not "X":
#                successors.append(below)
#        if node.pos_x > 0:
#            left = self.graph[node.pos_x-1][node.pos_y]
#            if left.tag is not "X":
#                successors.append(left)
#        if node.pos_y > 0:
#            above = self.graph[node.pos_x][node.pos_y-1]
#            if above.tag is not "X":
#                successors.append(above)
#        return successors
#    
#    #Find the distance between a node C
#    def calculate_arc_cost(self, C, P):
#        return 1


#Node class
class Vertex:
    def __init__(self, index, pos_x, pos_y, edges, color):
        self.index = index
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.edges = edges
        self.color = color
    

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

    #Execute algorithm with different amount of colors... This is bad code style
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


#Run the main function
main()
