#Written by johannsl 2015

#A star class
class AStar:
    def __init__(self, grid, search_type, distance_type):
        self.grid = grid
        self.search_type = search_type
        self.distance_type = distance_type

    #This method incrementally solves the problem
    def incremental_solver(self):
        return

    #This method completely solves the problem
    def complete_solver(self):
        
        #Initialize the algorithm
        closed_list = []
        open_list = []
        n0 = self.grid.grid[self.grid.a_pos_x][self.grid.a_pos_y]
        n0.g = 0

        #Check which method of calculating h to use, then set h and f
        if self.distance_type == "manhattan distance":
            n0.h = calculate_manhattan_distance(n0)
        else: n0.h = calculate_euclidian_distance(n0)
        n0.g + n0.h = n0.f
        open_list.append(n0)

        #Initiate main loop
        while open_list:
            x = open_list.pop()
            closed_list.append(x)

            #Look for end properties
            if x.tag == "B":
                path = []
                retracePath(path, x)
                return 

            #Look for neighbour nodes



    #This method calculates h using manhattan distance
    def calculate_manhattan_distance(self, ):
        return

    #This method calculates h using euclidian distance
    def calculate_euclidian_distance(self):
        return

