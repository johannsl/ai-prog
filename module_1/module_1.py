import a_star
import datetime
from graph import Graph
import gui
import os
import platform
import random
import re
import sys
import Tkinter as tk

# These are the global values
max_breadth = 250
max_height = 150

#The main function runs the basic terminal communication
def main():
    
    #Clear the screen, prepare the mainlopp, prepare the input file, and the input file list
    os.system("clear")
    flag = True
    f = open("input.txt", "r")
    file_list = []

    #Print welcome message including the premade graph information. Save the graph information as a list
    print ("Project Module #1: \n"
            "A Star \n"
            "\n"
            "Premade problems are:")
    
    print f.name
    for line in f.readlines():
        file_list.append(line)
        sys.stdout.write(line)
    
    print ("\n"
            "'Run 0-X' for premade problem \n"
            "'Run new' for custom problem \n"
            "'Speed test 0-X' for testing run speed \n"
            "'Exit' ends the script \n"
            "\n")

    #This is the mainloop - It reads input from the user and executes the commands
    while flag:
        the_input = raw_input(" > ")
        
        #Run a premade graph
        if the_input != "Run new" and the_input.startswith("Run"):

            #Get the correct premade graph and add the numbers to a list
            number = the_input[4:]
            line_list = map(int, re.findall(r'\d+', file_list[int(number)]))

            #Add the walls to a list
            walls = []
            for wall_start in range(7, len(line_list), 4):
                wall = []
                for wall_number in range(wall_start, wall_start+4):
                    wall.append(line_list[wall_number])
                walls.append(wall)
             
            #Initialize premade graph, and gui; If the graph is not too large
            if line_list[1] <= max_breadth and line_list[2] <= max_height:
                premade_graph = Graph(columns=line_list[1], rows=line_list[2], a_pos_x=line_list[3], a_pos_y=line_list[4], b_pos_x=line_list[5], b_pos_y=line_list[6], walls= walls)
                
                #Scale down the size if the graph is too large
                if line_list[1] > 50 and line_list[2] > 30:
                    size = 25/5
                else:
                    size = 25
                premade_graph_gui = gui.GUI(graph=premade_graph, cellsize=size)
                _run_gui(premade_graph_gui)
            else: print "Error: graph too large"

        #Run a custom graph
        elif the_input == "Run new":
            size = input("graph size: ")
            start = input("Start position: ")
            end = input("End position: ")
            walls = input("Wall positions: ")

            #Initialize custom graph, and gui; If the graph is not too large
            if size[0] <= max_breadth and size[1] <= max_height:
                custom_graph = Graph(columns=size[0],rows=size[1], a_pos_x=start[0], a_pos_y=start[1], b_pos_x=end[0], b_pos_y=end[1], walls=walls)

                #Scale down the size if the graph is too large
                if size[0] > 50 and size[1] > 30:
                    size = 25/5
                else:
                    size = 25
                custom_graph_gui = gui.GUI(graph=custom_graph, cellsize=size)
                _run_gui(custom_graph_gui)
            else: print "Error: graph too large"

        #Run a speed test for algorithm optimalization purposes
        elif the_input.startswith("Speed test"):
            number = the_input[11:]
            line_list = map(int, re.findall(r'\d+', file_list[int(number)]))

            #Add the walls to a list
            walls = []
            for wall_start in range(7, len(line_list), 4):
                wall = []
                for wall_number in range(wall_start, wall_start+4):
                    wall.append(line_list[wall_number])
                walls.append(wall)
             
            #Initialize the graph and run AStar
            graph = Graph(columns=line_list[1], rows=line_list[2], a_pos_x=line_list[3], a_pos_y=line_list[4], b_pos_x=line_list[5], b_pos_y=line_list[6], walls= walls)
            for run in range(10):
                search = a_star.AStar(graph)
                a = datetime.datetime.now()
                search.initialize("manhattan distance")
                result = search.complete_solver()
                b = datetime.datetime.now()
                print result[1], "\n", b-a

        #Exit the loop
        elif the_input == "Exit":
            flag = False
            f.close()
        
#Private run gui function aimed at making the program run more smoothly on Mac OS
def _run_gui(graph):
    if platform.system() == 'Darwin':
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            graph.mainloop()
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "iTerm" to true' ''')
    else: graph.mainloop()
    return

main()
