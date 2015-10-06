import node

class Graph:
    def __init__(self, columns, rows, a_pos_x, a_pos_y, b_pos_x, b_pos_y, walls):
        self.columns = columns
        self.rows = rows
        self.a_pos_x = a_pos_x
        self.a_pos_y = a_pos_y
        self.b_pos_x = b_pos_x
        self.b_pos_y = b_pos_y
        self.walls = walls
        self.graph = None
        self.n0 = None
         
        #Initialize the nodes in the graph
        graph = []
        for c in range(columns):
            row = []
            for r in range(rows):
                row.append(node.Node(tag="O", g=None, h=None, pos_x=c, pos_y=r, parent=None, kids=[], graph=self))
            graph.append(row)
        self.graph = graph
        
        #Set node tags
        graph[a_pos_x][a_pos_y].tag = "A"
        self.n0 = graph[a_pos_x][a_pos_y]
        graph[b_pos_x][b_pos_y].tag = "B"
        for wall in walls:
            for c in range(wall[0], wall[0]+wall[2]):
                for r in range(wall[1], wall[1]+wall[3]):
                    graph[c][r].tag = "X"

    #Check wether a node is the start
    def start_found(self, node):
        if node.tag == "A":
            return True
        return False

    #Check wether a node is the goal
    def goal_found(self, node):
        if node.tag == "B":
            return True
        return False
           
    #Find the distance between a node C
    def calculate_arc_cost(self, C, P):
        return 1
