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

##These are the global values

#The main function runs the basic terminal communication
def main():
    
    #Clear the screen, prepare the mainlopp, create graph_list, create graph_path
    os.system("clear")
    flag = True
    graph_path = "./graphs/"
    graph_list = os.listdir(graph_path)

    #Print welcome message including the premade graph information
    print """Project Module #2:
A*-GAC
    
Premade problems are:"""
    
    for i in range(len(graph_list)):
        print i, graph_list[i]
    print graph_list
    
    print """
'Run 0-X' for premade problem
'Run new' for custom problem
'Exit' ends the script
    """

    #This is the mainloop - It reads input from the user and executes the commands
    while flag:
        the_input = raw_input(" > ")
        
        #Run a premade graph
        if the_input != "Run new" and the_input.startswith("Run"):

            #Get the correct premade grid and add the numbers to a list
            number = the_input[4:]
            f = open("./graphs/" + str(graphs[int(number)]), "r")
            line_list = map(int, re.findall(r'\d+', f.readline()))
            
            nv = line_list[0]
            ne = line_list[1]
            verticies = []
            for i in range(nv):
                verticies.append(f.readline())
                print f.readline


            #line_list = map(int, re.findall(r'\d+', file_list[int(number)]))
            
            

            #print f.readline(1)
            #print f.readline(1)
            #verticies = [] 

#        #Run a speed test for algorithm optimalization purposes
#        elif the_input.startswith("Speed test"):
#            number = the_input[11:]
#            line_list = map(int, re.findall(r'\d+', file_list[int(number)]))

        #Exit the loop
        elif the_input == "Exit":
            flag = False
            f.close()
       
       
       
       
       
       
       
        
##Private run gui function aimed at making the program run more smoothly on Mac OS
#def _run_gui(grid):
#    if platform.system() == 'Darwin':
#            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
#            grid.mainloop()
#            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "iTerm" to true' ''')
#    else: grid.mainloop()
#    return
#
##Node class
#class Node:
#    def __init__(self, tag, g, h, f, pos_x, pos_y, parent, kids):
#        self.tag = tag
#        self.g = g
#        self.h = h
#        self.f = f
#        self.pos_x = pos_x
#        self.pos_y = pos_y
#        self.parent = parent
#        self.kids = kids
#    
#    #The nodes are to be sorted after their f value, or if they are similar, their h value
#    def __lt__(self, other):
#        if self.f == other.f:
#            return self.h < other.h
#        return self.f < other.f
#
##Grid class containing some problem specific help for the AStar class
#class Grid:
#    def __init__(self, columns, rows, a_pos_x, a_pos_y, b_pos_x, b_pos_y, walls):
#        self.columns = columns
#        self.rows = rows
#        self.a_pos_x = a_pos_x
#        self.a_pos_y = a_pos_y
#        self.b_pos_x = b_pos_x
#        self.b_pos_y = b_pos_y
#        self.walls = walls
#         
#        #Initialize the nodes in the grid
#        grid = []
#        for c in range(columns):
#            row = []
#            for r in range(rows):
#                row.append(Node(tag="O", g=None, h=None, f=None, pos_x=c, pos_y=r, parent=None, kids=[]))
#            grid.append(row)
#        self.grid = grid
#        
#        #Set node tags
#        grid[a_pos_x][a_pos_y].tag = "A"
#        grid[b_pos_x][b_pos_y].tag = "B"
#        for wall in walls:
#            for c in range(wall[0], wall[0]+wall[2]):
#                for r in range(wall[1], wall[1]+wall[3]):
#                    grid[c][r].tag = "X"
#       
#    #Find succeessors to a node in the grid and add them to a clockwise list
#    def generate_all_successors(self, node):
#        successors = []
#        if node.pos_x < self.columns-1:
#            right = self.grid[node.pos_x+1][node.pos_y]
#            if right.tag is not "X":
#                successors.append(right)
#        if node.pos_y < self.rows-1:
#            below = self.grid[node.pos_x][node.pos_y+1]
#            if below.tag is not "X":
#                successors.append(below)
#        if node.pos_x > 0:
#            left = self.grid[node.pos_x-1][node.pos_y]
#            if left.tag is not "X":
#                successors.append(left)
#        if node.pos_y > 0:
#            above = self.grid[node.pos_x][node.pos_y-1]
#            if above.tag is not "X":
#                successors.append(above)
#        return successors
#    
#    #Find the distance between a node C
#    def calculate_arc_cost(self, C, P):
#        return 1
#
##GUI is an interface subclass of Tkinter
#class GUI(tk.Tk):
#    def __init__(self, grid, cellsize):
#        tk.Tk.__init__(self)
#        self.grid = grid
#        self.search = None
#        
#        #Create the menu
#        menubar = tk.Menu(self)
#        execmenu = tk.Menu(menubar)
#        execmenu.add_command(label="Best-first search", command=self.best_first_search)
#        execmenu.add_command(label="Breadth-first search", command=self.breadth_first_search)
#        execmenu.add_command(label="Depth-first search", command=self.depth_first_search)
#        menubar.add_cascade(label="Exec", menu=execmenu)
#        self.config(menu=menubar)
#
#        #?Should a speed menu be added?
#        #speedmenu = tk.Menu(menubar)
#        #speedmenu.add_command(label="High speed", command=self.set_speed(100))
#        #speedmenu.add_command(label="Standard speed", command=self.set_speed(300))
#        #speedmenu.add_command(label="Low speed", command=self.set_speed(1000))
#        #menubar.add_cascade(label="Speed", menu=speedmenu)
#        
#        #Create a canvas to put the grid on. Set the size of boxes
#        self.cellwidth = cellsize
#        self.cellheight = cellsize
#        self.canvas = tk.Canvas(self, width=(grid.columns*self.cellwidth)+5, height=(grid.rows*self.cellheight)+5, borderwidth=10)
#        self.canvas.pack(side="top", fill="both", expand="true")
#        self.rectangle = {}
#        self.oval = {}
#
#        #Loop through the grid and paint boxes. Subtract y values from total rows to simulate the exercice grids
#        for r in range(grid.rows):
#            for c in range(grid.columns):
#                x1 = c * self.cellwidth
#                y1 = r * self.cellheight
#                x2 = x1 + self.cellwidth
#                y2 = y1 + self.cellheight
#                if grid.grid[c][grid.rows-r-1].tag == "O":
#                    self.rectangle[c, grid.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
#                    self.oval[c, grid.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, outline="white", tag="oval")
#                if grid.grid[c][grid.rows-r-1].tag == "X":
#                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")
#                if grid.grid[c][grid.rows-r-1].tag == "A":
#                    self.rectangle[c, grid.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
#                    self.oval[c, grid.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, tag="oval")
#                    if cellsize == 25:
#                        self.canvas.create_text(x1+12, y1+12, text="A")
#                if grid.grid[c][grid.rows-r-1].tag == "B":
#                    self.rectangle[c, grid.rows-r-1] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
#                    self.oval[c, grid.rows-r-1] = self.canvas.create_oval(x1+1, y1+1, x2-1, y2-1, outline="white", tag="oval")
#                    if cellsize == 25:
#                        self.canvas.create_text(x1+12, y1+12, text="B")
# 
#        #Place the window in the topmost left corner to prevent glitches in the gui
#        self.canvas.xview_moveto(0)
#        self.canvas.yview_moveto(0)
#
#    #Run best-first search
#    def best_first_search(self):
#        self.canvas.itemconfig("oval", fill="white", outline="white")
#        self.search = a_star.AStar(self.grid, "best-first", "manhattan distance", max_nodes)
#        self.redraw()
#
#    #Run breadth-first search
#    def breadth_first_search(self):
#        self.canvas.itemconfig("oval", fill="white", outline="white")
#        self.search = a_star.AStar(self.grid, "breadth-first", "manhattan distance", max_nodes)
#        self.redraw()
#
#    #Run depth-first search
#    def depth_first_search(self):
#        self.canvas.itemconfig("oval", fill="white", outline="white")
#        self.search = a_star.AStar(self.grid, "depth-first", "manhattan distance", max_nodes)
#        self.redraw()
#
#    #?Would a speed menu need this?
#    #Set the solver speed of the gui
#    #def set_speed(self, speed):
#    #    self.speed = speed
# 
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
#
##Run the main function
main()