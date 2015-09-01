#Written by johannsl 2015

import Tkinter as tk
import random
import os
import re
import platform
import sys
import a_star

#The main function runs the basic terminal communication
def main():
    
    #Clear the screen, prepare the mainlopp, prepare the input file, and the input file list
    os.system("clear")
    flag = True
    f = open("input.txt", "r")
    file_list = []

    #Print welcome message including the premade grid information. Save the grid information as a list
    print """Project Module #1:
A Star
    
Premade problems are:"""
    
    print f.name
    for line in f.readlines():
        file_list.append(line)
        sys.stdout.write(line)
    
    print """
'Run 0-X' for premade problem
'Run new' for custom problem
'Exit' ends the script
    """

    #This is the mainloop - It reads input from the user
    while flag:
        #the_input = raw_input(" > ")
        the_input = "Run 2"
        
        #Run a premade grid
        if the_input != "Run new" and the_input.startswith("Run"):

            #Get the correct premade grid and add the numbers to a list
            number = the_input[4:]
            line_list = map(int, re.findall(r'\d+', file_list[int(number)]))

            #Add the walls to a list
            walls = []
            for wall_start in range(7, len(line_list), 4):
                wall = []
                for wall_number in range(wall_start, wall_start+4):
                    wall.append(line_list[wall_number])
                walls.append(wall)
             
            #Initialize premade grid, and gui; If the grid is not too large
            if line_list[1] <= 50 and line_list[2] <=30:
                premade_grid = Grid(columns=line_list[1], rows=line_list[2], a_pos_x=line_list[3], a_pos_y=line_list[4], b_pos_x=line_list[5], b_pos_y=line_list[6], walls= walls)
                premade_grid_gui = GUI(grid = premade_grid)
                #_run_gui(premade_grid_gui)
            else: print "Error: Grid too large"
            flag = False
            f.close()

        #Run a custom grid
        elif the_input == "Run new":
            size = input("Grid size: ")
            start = input("Start position: ")
            end = input("End position: ")
            walls = input("Wall positions: ")

            #Initialize custom grid, and gui; If the grid is not too large
            if size[0] <= 50 and size[1] <= 30:
                custom_grid = Grid(columns=size[0],rows=size[1], a_pos_x=start[0], a_pos_y=start[1], b_pos_x=end[0], b_pos_y=end[1], walls=walls)
                custom_grid_gui = GUI(grid = custom_grid)
                _run_gui(custom_grid_gui)
            else: print "Error: Grid too large"

        #Exit the loop
        elif the_input == "Exit":
            flag = False
            f.close()
        
#Private run gui function
def _run_gui(grid):
    if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            grid.mainloop()
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "iTerm" to true' ''')
    else: grid.mainloop()
    return

#Node class
class Node:
    def __init__(self, tag, g, h, f, pos_x, pos_y, parent, kids):
        self.tag = tag
        self.g = g
        self.h = h
        self.f = f
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.parent = parent
        self.kids = kids

#Grid class
class Grid:
    def __init__(self, columns, rows, a_pos_x, a_pos_y, b_pos_x, b_pos_y, walls):
        self.columns = columns
        self.rows = rows
        self.a_pos_x = a_pos_x
        self.a_pos_y = a_pos_y
        self.b_pos_x = b_pos_x
        self.b_pos_y = b_pos_y
        self.walls = walls
         
        #Initialize the nodes in the grid
        grid = []
        for c in range(columns):
            row = []
            for r in range(rows):
                row.append(Node(tag="O", g=None, h=None, f=None, pos_x=c, pos_y=r, parent=None, kids=[]))
            grid.append(row)
        self.grid = grid
        
        #Set node tags
        grid[a_pos_x][a_pos_y].tag = "A"
        grid[b_pos_x][b_pos_y].tag = "B"
        for wall in walls:
            for c in range(wall[0], wall[0]+wall[2]):
                for r in range(wall[1], wall[1]+wall[3]):
                    grid[c][r].tag = "X"
        
        #Initialize the grid of nodes and flip the grid so it fits the exercice
        #ISSUE: When to flip the board?
        #grid = zip(*grid)[::-1]

        for r in range(rows):
            row = []
            for c in range(columns):
                row.append(grid[c][r].tag)
            print row

    #Find succeessors to a node in the grid and add them to a clockwise list
    def generate_all_successors(self, node):
        successors = []
        if node.pos_x > 0:
            left = self.grid[node.pos_x-1][node.pos_y]
            if left.tag is not "X":
                successors.append(left)
        if node.pos_y < self.rows-1:
            below = self.grid[node.pos_x][node.pos_y+1]
            if below.tag is not "X":
                successors.append(below)
        if node.pos_x < self.columns-1:
            right = self.grid[node.pos_x+1][node.pos_y]
            if right.tag is not "X":
                successors.append(right)
        if node.pos_y > 0:
            above = self.grid[node.pos_x][node.pos_y-1]
            if above.tag is not "X":
                successors.append(above)
        return successors
    
    #Find the distance between a node C
    def calculate_arc_cost(self, C, P):
        return 1

#GUI is a subclass of Tkinter
class GUI(tk.Tk):

    #Initialize GUI as itself and as Tkinter
    def __init__(self, grid):
        tk.Tk.__init__(self)
        self.grid = grid
        
        #Create the menu
        menubar = tk.Menu(self)
        execmenu = tk.Menu(menubar)
        execmenu.add_command(label="Best-first search", command=self.best_first_search)
        execmenu.add_separator()
        execmenu.add_command(label="Breadth-first search", command=self.breadth_first_search)
        execmenu.add_separator()
        execmenu.add_command(label="Depth-first search", command=self.depth_first_search)
        execmenu.add_separator()
        menubar.add_cascade(label="Exec", menu=execmenu)
        self.config(menu=menubar)
        
        #Set size and create cells according to the tag of the coordinate
        self.canvas = tk.Canvas(self, width=(grid.columns*25)+5, height=(grid.rows*25)+5, borderwidth=10)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.cellwidth = 25
        self.cellheight = 25
        self.rect = {}
        for c in range(grid.columns):
            for r in range(grid.rows):
                x1 = c * self.cellwidth
                y1 = r * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if grid.grid[r][c].tag == "O":
                    self.rect[c,r] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="open")
                if grid.grid[r][c].tag == "X":
                    self.rect[c,r] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", tags="wall")
                if grid.grid[r][c].tag == "A":
                    self.rect[c,r] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")
                    self.rect[c,r] = self.canvas.create_text(x1+12, y1+12, text="A", tags="start")
                    self.rect[c,r] = self.canvas.create_oval(x1, y1, x2, y2, tags="oval")
                if grid.grid[r][c].tag == "B":
                    self.rect[c,r] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="rect")
                    self.rect[c,r] = self.canvas.create_text(x1+12, y1+12, text="B", tags="end")
                    
        #Place the window in the topmost left corner to prevent glitches in the gui
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.best_first_search()
    
    #Run best-first search
    def best_first_search(self):
        search = a_star.AStar(self.grid, "best-first", "manhattan distance")
        print(search.complete_solver())

    #Run breadth-first search
    def breadth_first_search(self):
        raise NotImplementedError

    #Run depth-first search
    def depth_first_search(self):
        raise NotImplementedError

    
    #Redraw the gui
    def redraw():
        raise NotImplementedError

#Run the main function
main()
