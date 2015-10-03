#Written by johannsl and iverasp 2015
#This file contains classes, methods, and functions related to the specifications of Module #2

from csp import CSP
from gui import GUI
from graph import Graph
import datetime
import os
import platform
import random
import re
import sys
import Tkinter as tk
sys.path.append("..")
from project_module_1.a_star import AStar

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
        the_input = "Run 0"

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
