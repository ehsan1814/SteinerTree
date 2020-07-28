class Graph:
    def __init__(self , vertices):
        self.V = vertices   #Number of vertices
        self.graph = []     #List for store graph
    
    def addEdge(self , u , v , wieght):
        self.graph.append([u,v,wieght])