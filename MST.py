import os

class ReadWriteFile:
    def __init__(self, read_dir, write_dir=None):
        self.read_dir = read_dir
        if write_dir == None:
            self.write_dir = self.read_dir[0:-4] + ".out"
        else:
            self.write_dir = write_dir
        
        self.write_file()

    def read_file(self):
        number_of_nodes = 0
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
                    edges.append(Edge(min(u, v),max(u,v), wieght))

                
                if splited_line[i] == "T":
                    terminals.append(int(splited_line[i + 1]))
                
                i = i + 1

        file.close()
        return number_of_nodes, edges , terminals


    def write_file(self):
        number_of_nodes, edges , terminals = self.read_file()
        g1 = Graph(number_of_nodes)
        g1.set_graph(edges)
        g1.set_terminals(terminals)
        g1.make_MST()
        g1.make_steiner_tree()

        file = open(self.write_dir,"w")
        file.write("Cost of MST {}\n".format(g1.cost_of_mst))
        file.write("Cost of Steiner Tree {}\n".format(g1.cost_of_steiner_tree))
        file.write("Edges {}\n".format(len(g1.steiner)))
        
        for i in g1.steiner:
            file.write("E {} {} {}\n".format(i.u,i.v,i.wieght))
        
        file.close()
        

class Edge:
    def __init__(self, u, v, wieght=0):
        self.u = u
        self.v = v
        self.wieght = wieght

    def __getitem__(self,wieght):
        return self.wieght

    def __str__(self):
        return "{} {} - {}".format(self.u, self.v, self.wieght)
    
    def find_weight(self, list_of_edges):
        for i in list_of_edges:
            if self.u == i.u and self.v == i.v:
                return i.wieght


class Graph:
    def __init__(self, num_of_nodes):
        self.V = num_of_nodes   #Number of Nodes
        self.graph = []     #List for store edges 
        self.MST = []       #List for store Minimum Spannig Tree
        self.terminals = [] #List for save name of nodes that is terminal
        self.steiner = []   #List for store steiner tree
        self.cost_of_steiner_tree = 0
        self.cost_of_mst = 0
        
    
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
        self.cost_of_mst_function()

    def make_steiner_tree(self):
        
        '''
        List for save all nodes of a graph and thier wieght in MST 
        (This is helper to save nodes for make a steiner tree)
        '''
        nodes = [Node(-1,float("inf"))]

        ''' In this part we make array and add 
            each node to this array.'''
        for i in range(1, self.V + 1):
            nodes.append(Node(i))
        
        for i in self.terminals:
            nodes[i].is_terminal = True

        ''' In this part we traverse MST edges, 
            evaluate wieght of nodes
            and add each node to another node. 
        ''' 
        for j in self.MST:
            nodes[j.u].add_relation_node(j.v)
            nodes[j.v].add_relation_node(j.u)
    

        temp = []
        for a in nodes:
            temp.append(a)               
        
        for i in range(len(nodes) - 1):
            nodes = sorted(temp, key=lambda attribute: attribute[1])
            for j in nodes:
                if j.wieght_of_node == 1:
                    if not j.is_terminal:
                        for a in j.relation_nodes:
                            rel_node = a
                        temp[rel_node].delete_relation_node(j.name)
                        temp[j.name].delete_relation_node(rel_node)
                        temp[j.name].wieght_of_node = float("inf")


        self.steiner = temp
        self.make_steiner_tree_from_temp()
        self.cost_of_steiner_tree_function()
    
    def make_steiner_tree_from_temp(self):
        ls = []
        for i in self.steiner:
            for j in i.relation_nodes:
                minimum = min(i.name,j) 
                maximum = max(i.name,j)
                tuple = (minimum,maximum)
                if  tuple not in ls:
                    wieght1 = Edge(minimum,maximum).find_weight(self.graph)
                    ls.append(Edge(minimum,maximum,wieght1))
        self.steiner = ls

    def cost_of_steiner_tree_function(self):
        counter = 0
        for a in self.steiner:
            counter += a.wieght
        
        self.cost_of_steiner_tree = counter
    
    def cost_of_mst_function(self):
        counter = 0
        for a in self.MST:
            counter += a.wieght
        
        self.cost_of_mst = counter
                          
class Node:
    def __init__(self, name, wieght_of_node=0):
        self.name = name                     #This is name of the node     
        self.wieght_of_node = wieght_of_node #This is the wieght of the node
        self.relation_nodes = {}             #This is the nodes that we have an edge to them
        self.is_terminal = False

    def __getitem__(self,wieght_of_node):
        return self.wieght_of_node
    
    def __lt__(self, other):
        return self.wieght_of_node < other.wieght_of_node

    def add_relation_node(self, name_of_node):
        self.relation_nodes[name_of_node] = name_of_node
        self.add_wieght_of_node()
    
    def delete_relation_node(self, name_of_node):
        del self.relation_nodes[name_of_node]
        self.sub_wieght_of_node()
    
    def add_wieght_of_node(self):
        self.wieght_of_node = self.wieght_of_node + 1

    def sub_wieght_of_node(self):
        self.wieght_of_node = self.wieght_of_node - 1
    
    def __str__(self):
        return "name : {}-- wieght : {} -- rel : {}".format(self.name, self.wieght_of_node, self.relation_nodes)
    
    
#This part is for test
if __name__ == "__main__":
    for root, dirs, files in os.walk(".", topdown=False):
        for i in files:
            if i[-3:] == "stp":
                file = ReadWriteFile(i)
    