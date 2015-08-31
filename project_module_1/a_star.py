#Written by johannsl 2015

#A star class
class AStar:
    def __init__(self, grid, search_type, distance_type):
        self.grid = grid
        self.search_type = search_type
        self.distance_type = distance_type
        print "lol"

    #This method incrementally solves the problem
    def incremental_solver(self):
        return

    #This method completely solves the problem
    def complete_solver(self):

        #Initialize the algorithm
        closed_list = []
        open_list = []
        n0 = self.grid.grid[a_pos_x][a_pos_y]


    #This method calculates h using manhattan distance
    def calculate_manhattan_distance(self):
        return

    #This method calculates h using euclidian distance
    def calculate_euclidian_distance(self):
        return

