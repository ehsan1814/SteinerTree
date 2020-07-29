class ReadWriteFile:
    def __init__(self, read_dir, write_dir=None):
        self.read_dir = read_dir
        self.write_dir = write_dir
    
    def read_file(self):
        edges = []
        terminals = []
        
        file = open(self.read_dir, "w")
        for line in file:
            splited_line = line.split() 
            i = 0
            while i < len(splited_line):
                if splited_line[i] == "Nodes":
                    number_of_nodes = int(splited_line[i + 1])

                if splited_line[i] == "E":
                    u = splited_line[i + 1]
                    v = splited_line[i + 2]
                    wieght = splited_line[i + 3]
                    edges.append(Edge(u, v, wieght))

                if splited_line[i] == "Terminals":
                    try:
                        number_of_terminals = int(splited_line[i + 1])    
                    except IndexError :
                        break
                    
                    break
                
                if splited_line[i] == "T":
                    terminals.append(splited_line[i+1])

                i = i + 1
        file.close()
        return number_of_nodes, number_of_terminals, edges, terminals



    def write_file(self):
        pass


class Edge:
    def __init__(self, u, v, wieght):
        self.u = u
        self.v = v
        self.wieght = wieght

    def __getitem__(self,wieght):
        return self.wieght

    def __str__(self):
        return "{} {} - {}".format(self.u, self.v, self.wieght)


class Graph:
    def __init__(self, vertices):
        self.V = vertices   #Number of vertices
        self.graph = []     #List for store graph
    
    
    #This function for add Edge
    def add_edge_to_graph(self, u, v, wieght):
        self.graph.append(Edge(u, v, wieght))


    #This function for find parent of verticle
    #Use path compression way 
    def find_parent(self, parent, i):
        if parent[i] == i :
            return i 
        return self.find_parent(parent, parent[i])

    #This function is for union two sets of x and y
    def union(self, parent, rank, x, y):
        xParent = self.find_parent(parent, x)
        yParent = self.find_parent(parent, y)
 
        
        if rank[xParent] < rank[yParent]: 
            parent[xParent] = yParent 
        elif rank[xParent] > rank[yParent]: 
            parent[yParent] = xParent 

        else :
            parent[yParent] = xParent
            rank[xParent] += 1
        
    
    def make_MST(self):
        
        result = [] #This is for save MST 

        i = 0
        e = 0

        #This is for sort edges based on weight
        self.graph = sorted(self.graph, key=lambda attribute: attribute[2])

        parent = [] 
        rank = [] 

        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        
        while e < self.V - 1 :
            edge = self.graph[i]
            u,v,wieght = edge.u, edge.v, edge.wieght
            i = i + 1

            x = self.find_parent(parent, u)
            y = self.find_parent(parent, v)

            if x != y:
                e = e + 1
                result.append(Edge(u,v,wieght))
                self.union(parent, rank, x, y)

        return result
                



#This part is for test
if __name__ == "__main__":
    '''graph = Graph(4)
    graph.graph = [Edge(0,1,0), Edge(0,2,1), Edge(0,3,5), Edge(1,3,1)]
    res = graph.make_MST()
    for a in res:
        print(a)'''

    a = ReadWriteFile("cc6-2p.stp")
    print(a.read_dir)
    a.read_file()
    #print(w,x,y,z,sep="\n")
    
    
    
