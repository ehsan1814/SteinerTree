class ReadWriteFile:
    def __init__(self, read_dir, write_dir=None):
        self.read_dir = read_dir
        if write_dir == None:
            self.write_dir = self.read_dir[0:-3] + ".out"
        else:
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
        file = open(self.write_dir)
        file.close()
        

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
    def __init__(self, num_of_nodes):
        self.V = num_of_nodes   #Number of Nodes
        self.graph = []     #List store edges in a list 
        self.MST = []       #List for store Minimum Spannig Tree
        self.terminals = [] #List for save name of nodes that is terminal
        
        '''
        List for save all nodes of a graph and thier wieght in MST 
        (This is helper to save nodes for make a steiner tree)
        '''
        self.nodes = [Node(-1,float("inf"))]   
        
    
    #Setter method for terminals
    def set_terminals(self, list_of_terminals):
        self.terminals = list_of_terminals

    #Getter method for terminals
    def get_terminals(self):
        return self.terminals

    #Setter method for graph
    def set_graph(self, list_of_edges):
        self.graph = list_of_edges
    
    #Getter method for graph
    def get_graph(self):
        return self.graph

    #This function for add Edge
    def add_edge_to_graph(self, u, v, wieght):
        self.graph.append(Edge(u, v, wieght))

    '''This function for find parent of verticle
        Use path compression way '''
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
        
    #This function make minimum spannig tree
    def make_MST(self):
        
        result = [] #This is for save MST(Save all edges in MST)

        i = 0 #This is index for sorted edges to make a MST
        e = 0 #This is for edges that check the rule for tree

        #This is for sort edges based on weight
        self.graph = sorted(self.graph, key=lambda attribute: attribute[2])

        parent = [] #This is show parent of each node
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

        self.MST = result

    def make_steiner_tree(self):

        ''' In this part we make array and add 
            each node to this array.'''
        for i in range(1, self.V + 1):
            self.nodes.append(Node(i))
        
        for j in self.MST:
            self.nodes[j.u].add_relation_node(j.v)
            self.nodes[j.v].add_relation_node(j.u)
            self.nodes[j.u].add_wieght_of_node()
            self.nodes[j.v].add_wieght_of_node()

        # i = 1  #this part for test
        # for a in self.nodes :
        #     print("In the func" ,i , a.wieght_of_node , sep = " - ")
        #     i = i + 1

        self.nodes = sorted(self.nodes, key=lambda attribute: attribute[1])

        
                   
class Node:
    def __init__(self, name, wieght_of_node=0):
        self.name = name                     #This is name of the node     
        self.wieght_of_node = wieght_of_node #This is the wieght of the node
        self.relation_nodes = []             #This is the nodes that we have an edge to them

    def __getitem__(self,wieght_of_node):
        return self.wieght_of_node

    def add_relation_node(self, name_of_node):
        self.relation_nodes.append(name_of_node)
    
    def add_wieght_of_node(self):
        self.wieght_of_node = self.wieght_of_node + 1

    def sub_wieght_of_node(self):
        self.wieght_of_node = self.wieght_of_node - 1
    
    
#This part is for test
if __name__ == "__main__":
    
    a = ReadWriteFile("cc6-2p.stp")
    number_of_nodes, edges , number_of_terminals, terminals = a.read_file()
    graph = Graph(number_of_nodes)
    graph.set_graph(edges)
    i = 1
    graph.make_MST()
    graph.make_steiner_tree()
    for a in graph.nodes :
        print(i , a.wieght_of_node , sep = " - ")
        i = i + 1
    # graph.set_terminals(terminals)
    # print(graph.terminals)
    # i = 1
    # for a in graph.MST :
    #     print(i , a , sep=" -- ")
    #     i =  i +  1
    
    
    
