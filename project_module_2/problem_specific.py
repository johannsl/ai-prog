#Written by johannsl 2015
#This file contains classes, methods, and functions related to the specifications of Module #2

import a_star
import datetime
import os
import platform
import random
import re
import sys
import Tkinter as tk


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
            "'Run new' for custom problem \n"
            "'Exit' ends the script \n"
            "\n")

    #This is the mainloop - It reads input from the user and executes the commands
    while flag:
        the_input = raw_input(" > ")
        
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
                vertex = map(int, re.findall(r'\d+', f.readline()))
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


#Graph class containing some problem specific help for the AStar class
class Graph:
    def __init__(self, NV, NE, verticies, edges):
        self.NV = NV
        self.NE = NE
        self.verticies = verticies
        self.edges = edges
         
        #Initialize the nodes in the graph
        graph = []
        for vertex in verticies:
            graph.append(Vertex(index=vertex, pos_x=vertex[1], pos_y=vertex[2], color=None))
        self.graph = graph
        
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
    def __init__(self, index, pos_x, pos_y, color):
        self.index = index
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
    

##GUI is an interface subclass of Tkinter
class GUI(tk.Tk):
    def __init__(self, graph):
        tk.Tk.__init__(self)
        self.graph = graph
        
        #Create the menu
        menubar = tk.Menu(self)
        execmenu = tk.Menu(menubar)
        execmenu.add_command(label="Execute!", command=self.execute)
        menubar.add_cascade(label="Exec", menu=execmenu)
        self.config(menu=menubar)

        #Create a canvas to put the graph on. Set the size of boxes
        self.canvas = tk.Canvas(self, width=800, height=800, borderwidth=10)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rectangle = {}
        self.oval = {}

#        #Loop through the graph and paint boxes. Subtract y values from total rows to simulate the exercice graphs
#        for r in range(graph.rows):
#            for c in range(graph.columns):
#                x1 = c * self.cellwidth
#                y1 = r * self.cellheight
#                x2 = x1 + self.cellwidth
#                y2 = y1 + self.cellheight
#                if graph.graph[c][graph.rows-r-1].tag == "O":
#                    self.rectangle[c, graph.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
#                    self.oval[c, graph.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, outline="white", tag="oval")
#                if graph.graph[c][graph.rows-r-1].tag == "X":
#                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
#                if graph.graph[c][graph.rows-r-1].tag == "A":
#                    self.rectangle[c, graph.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
#                    self.oval[c, graph.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, tag="oval")
#                    if cellsize == 25:
#                        self.canvas.create_text(x1+12, y1+12, text="A")
#                if graph.graph[c][graph.rows-r-1].tag == "B":
#                    self.rectangle[c, graph.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
#                    self.oval[c, graph.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, outline="white", tag="oval")
#                    if cellsize == 25:
#                        self.canvas.create_text(x1+12, y1+12, text="B")
# 
#        #Place the window in the topmost left corner to prevent glitches in the gui
#        self.canvas.xview_moveto(0)
#        self.canvas.yview_moveto(0)
#
    #Execute algorithm
    def execute(self):
        return

#    #Draws the gui with nodes from the open, closed, and complete path list
#    def redraw(self):
#        result = self.search.incremental_solver()
#
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
#
#        #Delay before next drawing phase
#        self.after(update_speed, lambda: self.redraw())


#Run the main function
main()
