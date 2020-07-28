class Graph:
    def __init__(self, vertices):
        self.V = vertices   #Number of vertices
        self.graph = []     #List for store graph
    
    
    #This function for add Edge
    def addEdge(self, u, v, wieght):
        self.graph.append([u, v, wieght])


    #This function for find parent of verticle
    #Use path compression technique
    def find(self, parent, i):
        if parent[i] == i :
            return i 
        return self.find(parent, parent[i])

    #This function is for union two sets of x and y
    def union(self, parent, rank, x, y):
        xParent = self.find(parent, x)
        yParent = self.find(parent, y)
 
        
        if rank[xParent] < rank[yParent]: 
            parent[xParent] = yParent 
        elif rank[xParent] > rank[yParent]: 
            parent[yParent] = xParent 

        else :
            parent[yParent] = xParent
            rank[xParent] += 1
        
    