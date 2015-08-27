#Written by johannsl 2015

#The Node class represents nodes and their values. The tag is the location of the character in the string. I use the tag to easily identify which and where each node is.
class Node:
    def __init__(self, tag, g, h, posX, posY, parent, kids):
        self.t = tag
        self.g = g
        self.h = h
        self.f = g + h
        self.x = posX
        self.y = posY
        self.p = parent
        self.k = kids

#The Graph class represents graphs and their values.
class Graph:
    def __init__(self, tag, graph, rows, columns, aTag, aPosX, aPosY, bTag, bPosX, bPosY):
        self.tag = tag
        self.graph = graph
        self.rows = rows
        self.columns = columns
        self.aTag = aTag
        self.aPosX = aPosX
        self.aPosY = aPosY
        self.bTag = bTag
        self.bPosX = bPosX
        self.bPosY = bPosY

#This is the A* implementation.
def aStar(Graph):
    G = Graph

    #----------------
    #Print Graph test:
    print G.graph
    #----------------
    
    #Initialize the algorithm:
    closedList = []
    openList = []
    n0 = Node(G.aTag, 0, (G.bPosX-G.aPosX)+(G.bPosY-G.aPosY), G.aPosX, G.aPosY, None, [])
    openList.append(n0)
    
    #Initialize the mainloop:
    while len(openList) is not 0:

    #----------------------
    #Set loops test:
    #for loops in range(40):
    #----------------------

        X = openList.pop()
        closedList.append(X)
        
        #-------------------------
        #Print X-values test:
        #print X.t, X.x, X.y, X.f
        #-------------------------
        
        #Checking for end properties:
        if X.t == G.bTag:
            path = []
            retracePath(path, X, G)
            return "SUCCESS"
        
        #Calculate successors (to reach the nodes over or under X, one needs to substract or add (the number of rows +1) in my implementation. This is because of the String method I am using).
        succ = []
        #The node left of X
        s1 = Node(X.t-1, X.g+1, abs(G.bPosX-(X.x-1))+abs(G.bPosY-X.y), X.x-1, X.y, X, [])
        #check if s1 is legal
        if s1.x >= 0:
            if G.graph[s1.t] is "." or G.graph[s1.t] is "B":
                 succ.append(s1)
        #The node over X
        s2 = Node(X.t-(G.rows+1), X.g+1, abs(G.bPosX-X.x)+abs(G.bPosY-(X.y-1)), X.x, X.y-1, X, [])
        #check if s2 is legal
        if s2.y >= 0:
            if G.graph[s2.t] is "." or G.graph[s2.t] is "B":
                succ.append(s2)
        #The node right of X
        s3 = Node(X.t+1, X.g+1, abs(G.bPosX-(X.x+1))+abs(G.bPosY-X.y), X.x+1, X.y, X, [])
        #check if s3 is legal
        if s3.x < G.rows:
            if G.graph[s3.t] is "." or G.graph[s3.t] is "B":
                succ.append(s3)
        #The node under X
        s4 = Node(X.t+(G.rows+1), X.g+1, abs(G.bPosX-X.x)+abs(G.bPosY-(X.y+1)), X.x, X.y+1, X, [])
        #check if s4 is legal
        if s4.y < G.columns:
            if G.graph[s4.t] is "." or G.graph[s4.t] is "B":
                succ.append(s4)
       
        #-------------------------
        #Successor test: 
        #tempListS = []
        #for s in succ:
        #    tempListS.append(s.t)
        #print "succ: ",tempListS
        #---------------------------
        
        #Here I check whetever I've encountered the node before. If it is in the closedList or openList, I simply flag the iteration so I don't add it to the openList yet again. If there are improvements in g, I add these. If there is an improvement in a node in the closedList, I run pathImprove to improve the paths to all kids of the node.
        for s in succ:
            flag = False
            X.k.append(s)
            for c in closedList:
                if s.t == c.t:
                    if s.f < c.f:
                        c.p = s.p
                        c.g = s.g
                        pathImprove(s)
                    flag = True
                    break
            if flag == True:
                continue
            for o in openList:
                if s.t == o.t:
                    if s.f < o.f:
                        o.p = s.p
                        o.g = s.g
                    flag = True
                    break
            if flag == True:
                continue
            #If I have not encoutered the node before, I simply add it to openList.
            openList.append(s)
        #openList is sorted to easily pop the most valuable node.
        openList.sort(key=lambda x: x.f, reverse=True)

        #-----------------------------
        #Open and closed list test:
        #tempListO = []
        #tempListC = []
        #for i in openList:
        #    tempListO.append(i.t)
        #for j in closedList:
        #    tempListC.append(j.t)
        #print "open: ", tempListO
        #print "closed: ", tempListC, "\n"
        #----------------------------------        

    return "FAIL"

#This function improves the g-value of all child nodes of P iteratively.
def pathImprove(P):
    for k in P.k:
        if P.g + 1 < k.g:
            k.p = P
            k.g = P.g + 1
            pathImprove(k)

#The retracePath function is called upon at a success. It prints a graph where the best path from A to B is marked with o's.
def retracePath(path, current, G):
    if current.t == G.aTag:
        B = G.graph
        for p in path:
            if p.t is not G.aTag:
                B = B[:p.t] + "o" + B[p.t+1:]
        print B
    else:
        path.append(current.p)
        retracePath(path, current.p, G)
