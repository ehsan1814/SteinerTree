class ReadWriteFile:
    def __init__(self, read_dir, write_dir=None):
        self.read_dir = read_dir
        self.write_dir = write_dir
    
    def read_file(self):
        number_of_nodes = 0
        number_of_terminals = 0
        edges = []
        terminals = []
        
        file = open(self.read_dir, "r")
        for line in file:
            splited_line = line.split() 
            i = 0
            while i < len(splited_line):
                if splited_line[i] == "Nodes":
                    number_of_nodes = int(splited_line[i + 1])

                if splited_line[i] == "E":
                    u = int(splited_line[i + 1])
                    v = int(splited_line[i + 2])
                    wieght = int(splited_line[i + 3])
                    edges.append(Edge(u, v, wieght))

                if splited_line[i] == "Terminals":
                    try:
                        number_of_terminals = int(splited_line[i + 1])    
                    except IndexError :
                        break
                    
                    break
                
                if splited_line[i] == "T":
                    terminals.append(int(splited_line[i + 1]))
                
                i = i + 1

        file.close()
        return number_of_nodes, edges , number_of_terminals, terminals



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

        for node in range(self.V + 1):
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
    a = ReadWriteFile("cc6-2p.stp")
    number_of_nodes, edges , number_of_terminals, terminals = a.read_file()
    graph = Graph(number_of_nodes)
    graph.graph = edges
    i = 1
    for a in graph.make_MST() :
        print(i , a , sep="--")
        i =  i +  1
    
    
    
