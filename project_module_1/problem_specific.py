#Written by johannsl 2015

import Tkinter as tk
import random
import os
import re
import platform
import sys

#The main function runs the basic terminal communication
def main():
    
    #Clear the screen, prepare the mainlopp, prepare the input file, and the input file list
    os.system("clear")
    flag = True
    f = open("input.txt", "r")
    fileList = []

    #Print welcome message including the premade grid information. Save the grid information as a list
    print """Project Module #1:
A Star
    
Premade problems are:"""
    
    print f.name
    for line in f.readlines():
        fileList.append(line)
        sys.stdout.write(line)
    
    print """
'Run 0-X' for premade problem
'Run new' for custom problem
'Exit' ends the script
    """

    #This is the mainloop - It reads input from the user
    while flag:
        the_input = raw_input(" > ")

        #Run a premade grid
        if the_input != "Run new" and the_input.startswith("Run"):

            #Get the correct premade grid and add the numbers to a list
            number = the_input[4:]
            lineList = map(int, re.findall(r'\d+', fileList[int(number)]))

            #Add the walls to a list
            walls = []
            for wallStart in range(7, len(lineList), 4):
                wall = []
                for wallNumber in range(wallStart, wallStart+4):
                    wall.append(lineList[wallNumber])
                walls.append(wall)
             
            #Initialize premade grid, and gui; If the grid is not too large
            if lineList[1] <= 50 and lineList[2] <=30:
                premadeGrid = Grid(columns=lineList[1], rows=lineList[2], aPosX=lineList[3], aPosY=lineList[4], bPosX=lineList[5], bPosY=lineList[6], walls= walls)
                premadeGridGui = GUI(grid = premadeGrid)
                _run_gui(premadeGridGui)
            else: print "Error: Grid too large"
            #flag = False
            #f.close()

        #Run a custom grid
        elif the_input == "Run new":
            size = input("Grid size: ")
            start = input("Start position: ")
            end = input("End position: ")
            walls = input("Wall positions: ")

            #Initialize custom grid, and gui; If the grid is not too large
            if size[0] <= 50 and size[1] <= 30:
                customGrid = Grid(columns=size[0],rows=size[1], aPosX=start[0], aPosY=start[1], bPosX=end[0], bPosY=end[1], walls=walls)
                customGridGui = GUI(grid = customGrid)
                _run_gui(customGridGui)
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
    def __init__(self, tag, g, h, f, posX, posY, parent, kids):
        self.tag = tag
        self.g = g
        self.h = h
        self.f = f
        self.posX = posX
        self.posY = posY
        self.parent = parent
        self.kids = kids

#Grid class
class Grid:
    def __init__(self, columns, rows, aPosX, aPosY, bPosX, bPosY, walls):
        self.columns = columns
        self.rows = rows
        self.aPosX = aPosX
        self.aPosY = aPosY
        self.bPosX = bPosX
        self.bPosY = bPosY
        self.walls = walls
         
        #Initialize the nodes in the grid
        grid = []
        for c in range(columns):
            row = []
            for r in range(rows):
                row.append(Node(tag="O", g=None, h=None, f=None, posX=c, posY=r, parent=None, kids=None))
            grid.append(row)
        
        #Set node tags
        grid[aPosX][aPosY].tag = "A"
        grid[bPosX][bPosY].tag = "B"
        for wall in walls:
            for c in range(wall[0], wall[0]+wall[2]):
                for r in range(wall[1], wall[1]+wall[3]):
                    grid[c][r].tag = "X"
        
        #Initialize the grid of nodes and flip the grid so it fits the exercice
        grid = zip(*grid)[::-1]
        self.grid = grid
        
#GUI is a subclass of Tkinter
class GUI(tk.Tk):

    #Initialize GUI as itself and as Tkinter
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args)
        grid = kwargs.pop("grid")
        
        #Create the menu
        menubar = tk.Menu(self)
        execmenu = tk.Menu(menubar)
        execmenu.add_command(label="Best-first search", command=self.best_first_search)
        execmenu.add_separator()
        execmenu.add_command(label="Depth-first search", command=self.depth_first_search)
        execmenu.add_separator()
        execmenu.add_command(label="Breadth-first search", command=self.breadth_first_search)
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
    
    #Run best-first search
    def best_first_search(self):
        raise NotImplementedError

    #Run depth-first search
    def depth_first_search(self):
        raise NotImplementedError

    #Run breadth-first search
    def breadth_first_search(self):
        raise NotImplementedError
    
    #Redraw the gui
    def redraw():
        raise NotImplementedError

#Run the main function
main()
