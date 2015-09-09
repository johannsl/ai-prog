import heapq

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

   # def __eq__(self, other):
   #     print "lol"
   #     return other.f == self.f

    def __lt__(self, other):
        print "lol1"
        return self.f < other.f

   # def __le__(self, other):
   #     print "lol2"
   #     return self.f < other.f

   # def __ne__(self, other):
   #     print "lol3"
   #     return self.f != other.f

   # def __gt__(self, other):
   #     print "lol4"
   #     return self.f < other.f

   # def __ge__(self, other):
   #     print "lol5"
   #     return self.f < other.f

    #def __cmp__(self, other):
    #    return cmp(self.f, other.f)

openHeap = []

for i in range(10,0,-1):
    node = Node("lol", 0, 0, i, 0, 0, None, None)
    heapq.heappush(openHeap, node)

for j in openHeap:
    print j.f

print "\n\n"

print heapq.heappop(openHeap).f
print heapq.heappop(openHeap).f
print heapq.heappop(openHeap).f
print heapq.heappop(openHeap).f

#print len(openHeap)
#print "Also here"
#print openHeap[0].f, openHeap[1].f
#print openHeap[0] > openHeap[1]
