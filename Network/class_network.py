import numpy as np
import networkx as nx
import math
import random
import matplotlib.pyplot as plt
from class_node import Node

def id_edges(z):
##return a dictionnary associating to each edge the nodes concerned. used for M2
    d={}
    x=0 
    y=0
    for i in range (0,int(z)):
        if(x<y):
            d[i]=(y,x)
            x+=1
        else:
            y+=1
            x=0
            d[i]=(y,x)
            x+=1
    return(d) 

def check_network_method(network_method):
    ##check the coherence of the input network_method 
    #doesn't really work for now...
    network_M = network_method 
    if type(network_M) != list:
        print('Error with the input network_methode')

    if(network_M[0] != 'M1' or network_M[0] != 'M2' or network_M[0] != 'M3'):
        print('Error with the input network_methode')

    if (network_M[0] == 'M1'):
        if (len(network_M) > 1):
            print('Error with the input network_methode')

    if (network_M[0] == 'M2'):
        if (len(network_M) < 3):
            print('Error with the input network_methode')
        if (network_M[1] != 'Poisson' or network_M[1] != 'Uniform' or network_M[1] != 'Normal' ):
            print('Error with the input network_methode')
        if (network_M[1] == 'Poisson' and len(network_M) > 3):
            print('Error with the input network_methode')
        if (network_M[1] == 'Uniform' or network_M[1] == 'Normal'):
            if (len(network_M) != 4 or network_M[3]<0):
                print('Error with the input network_methode')

    if (network_M[0] == 'M3'):
        pass
    return network_M



class Network:
    def __init__(self, num_nodes, interactions_per_node, hawk_dove_payoff, memory_cost, initial_memory_poisson, initial_aggression, network_methode):
        self.num_nodes = num_nodes # an int
        self.interactions_per_node = interactions_per_node # an int
        self.payoff_matrix = hawk_dove_payoff #[hawk-hawk winner, hawk-hawk loser, hawk-dove hawk, hawk-dove dove; dove-dove dove]
        self.memory_cost = memory_cost #metabolic cost of each memory slot, paid after each interaction
        self.nodes = [] #list of Node objects of the network
        self.history = [] #after every refresh, save the average fitness, memory, and aggression
        self.memory_history = [] # memories sL-sW for one generation every interaction initial sL-sW = 1
        self.fitness_history = []   # memories fitness for one generation every interaction
        memory = np.random.poisson(initial_memory_poisson, size = self.num_nodes) #initial memory is a poisson distribution
        #memory = [initial_memory_poisson]*self.num_nodes #we fix the memory 
        aggression = np.random.normal(initial_aggression, 0.05, self.num_nodes) #initial aggression is a Gaussian(loc, 0.05)
        #aggression = [initial_aggression]*self.num_nodes #we fix aggression for the moment
        #sizes = np.random.random_sample(self.num_nodes) #generate uniform sample of sizes list, each node has a 'size'
        
        #self.network_methode = check_network_method(network_methode) #list with first element the methode, second the mode, 3rd mean, 4th para
        self.network_methode = network_methode
        #create inital Nodes
        for i in range(self.num_nodes):
            #self.nodes.append(Node(sizes[i], memory[i], aggression[i]))
            self.nodes.append(Node(i/(self.num_nodes-1), memory[i], aggression[i])) #the size is: i/(self.num_nodes-1)
            self.fitness_history.append([self.nodes[i].fitness]) #fill the initial fitness of each fish (0)
            self.memory_history.append([self.nodes[i].max_size-self.nodes[i].min_size])
        if (self.network_methode[0] == 'M1' or self.network_methode[0] == 'M2'):
            self.graphs = [nx.MultiGraph()] #list of each generation's graph
            self.Max_edges = self.num_nodes*(self.num_nodes-1)/2 #the id Max that an edge can get
            for i in range(num_nodes):
                self.graphs[0].add_node(i,key=i)
            self.id_edges = id_edges(self.Max_edges)
        if (self.network_methode[0] == 'M3'):
            if (self.network_methode[1] == 'Erdos-Renyi'):
                self.Max_edges = self.network_methode[2]
                self.graphs = [nx.gnm_random_graph(num_nodes, self.Max_edges)]
            if (self.network_methode[1] == 'Small-world'):
                self.graphs = [nx.watts_strogatz_graph(num_nodes, self.network_methode[2], self.network_methode[3])]
                self.Max_edges = len(self.graphs[0].edges())
                
             
    def interact(self):    
        #by default each node has the same probability of having an interaction, with all nodes equally likely to interact with all other nodes
        #otherwise we use the poisson distribution or Uniform distribution to generate probabilities of picking edges
        
        if (self.network_methode[0] == 'M1'): #completely random case 
            indices = np.random.choice(self.num_nodes, size = (int(self.interactions_per_node*self.num_nodes/2), 2)) #pick 2 possible nodes to interact
            for i in range(int(self.interactions_per_node*self.num_nodes/2)): #/2 by two because with one edge 2individuals interact
                ind1 = indices[i][0]
                ind2 = indices[i][1]
                if ind1 != ind2: #check for interaction with self
                    self.hawk_dove(self.nodes[ind1], self.nodes[ind2]) 
                else: #assign new partner if assigned an interaction with self
                    ind2 = np.random.choice([index for index in np.arange(self.num_nodes) if index != ind1])
                    self.hawk_dove(self.nodes[ind1], self.nodes[ind2])   
                self.graphs[len(self.graphs)-1].add_edge(ind1,ind2)
            
                #memories fitness and SL-sW 
                self.memory_history[ind1].append(self.nodes[ind1].max_size-self.nodes[ind1].min_size)
                self.memory_history[ind2].append(self.nodes[ind2].max_size-self.nodes[ind2].min_size)
                self.fitness_history[ind1].append(self.nodes[ind1].fitness)
                self.fitness_history[ind2].append(self.nodes[ind2].fitness)

        elif (self.network_methode[0] == 'M2'): # in this case we add weights to edges according to the poisson or Normal distribution
            if (self.network_methode[1] == 'Poisson'):
                distribution = np.random.poisson(self.network_methode[2], int(self.Max_edges))
            if (self.network_methode[1] == 'Uniform'):
                L = self.network_methode[2]-math.sqrt(3*self.network_methode[3])
                H = self.network_methode[2]+math.sqrt(3*self.network_methode[3])+1
                distribution = np.random.randint(np.round(L),np.round(H),int(self.Max_edges))
            if (self.network_methode[1] == 'Normal'):
                distribution = np.random.normal(self.network_methode[2], self.network_methode[3], int(self.Max_edges))
            distribution = distribution/np.sum(distribution)
            edges = np.random.choice(int(self.Max_edges), int(self.interactions_per_node*self.num_nodes/2), p = distribution) #we select self.interactions_per_node*self.num_nodes edges from 0 to self.Max_edges
            for edge in edges:
                [ind1,ind2] = self.id_edges[edge]
                self.graphs[len(self.graphs)-1].add_edge(ind1,ind2)
                self.hawk_dove(self.nodes[ind1], self.nodes[ind2])

                #memories fitness and SL-sW 
                self.memory_history[ind1].append(self.nodes[ind1].max_size-self.nodes[ind1].min_size)
                self.memory_history[ind2].append(self.nodes[ind2].max_size-self.nodes[ind2].min_size)
                self.fitness_history[ind1].append(self.nodes[ind1].fitness)
                self.fitness_history[ind2].append(self.nodes[ind2].fitness)

        elif (self.network_methode[0] == 'M3'):
            for i in range(int(self.interactions_per_node*self.num_nodes/2)):
                edge = random.randint(0, self.Max_edges-1)
                edges = list(self.graphs[0].edges())
                (ind1, ind2) = edges[edge]
                self.hawk_dove(self.nodes[ind1], self.nodes[ind2])
                #memories fitness and SL-sW 
                self.memory_history[ind1].append(self.nodes[ind1].max_size-self.nodes[ind1].min_size)
                self.memory_history[ind2].append(self.nodes[ind2].max_size-self.nodes[ind2].min_size)
                self.fitness_history[ind1].append(self.nodes[ind1].fitness)
                self.fitness_history[ind2].append(self.nodes[ind2].fitness) 

        #Every Node pays a cost per memory slot after every time step (even if they haven't interacted)
        for node in self.nodes:
            node.fitness -= len(node.size_memory)*self.memory_cost
            if (node.fitness < 0):
                node.fitness = 0

        
    def hawk_dove(self, node1, node2):
        #increment the total number of interactions a Node has had over its lifetime
        node1.num_interactions += 1
        node2.num_interactions += 1
        
        #these numbers are used to determine if an ignorant Node plays hawk or dove
        rand_nums = np.random.random_sample(2)
        
        #If a Node remembers beating a bigger Node than its current partner, it plays hawk;
        #If a Node remembers losing to a smaller Node than its current partner, it plays dove;
        #Otherwise, we label the Node as ignorant, its probability of playing hawk is its aggression
        #Victories are stored in memory as 1 and losses as 0, if there was not a hawk-hawk interaction,
        #the interaction still uses a memory slot, but it is recorded as None.
        
        if node2.size < node1.min_size: #player 1 plays hawk
            if node1.size < node2.min_size: #player 2 plays hawk
                if node1.size > node2.size: #player 1 wins
                    node1.fitness += self.payoff_matrix[0]
                    node2.fitness += self.payoff_matrix[1]
                    node1.add_memory(node2.size, 1)
                    node2.add_memory(node1.size, 0)
                    #print('player 1 wins, player 2 hawk')
                else: #player 2 wins
                    node2.fitness += self.payoff_matrix[0]
                    node1.fitness += self.payoff_matrix[1]
                    node1.add_memory(node2.size, 0)
                    node2.add_memory(node1.size, 1)
                    #print('player 2 wins, both are hawk')
            elif node1.size > node2.max_size: #player 2 plays dove
                node1.fitness += self.payoff_matrix[2]
                node2.fitness += self.payoff_matrix[3]
                node1.add_memory(node2.size, None)
                node2.add_memory(node1.size, None)
                #print('player 2 dove, player 1 hawk')
            else: #player 2 ignorant
                if node2.aggression > rand_nums[1]: #player 2 plays ignorant hawk if level of agression of the player is high 'enough' -> maybe we want to change this?
                    if node1.size > node2.size: #player 1 wins
                        node1.fitness += self.payoff_matrix[0]
                        node2.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 1)
                        node2.add_memory(node1.size, 0)
                        #print('player 1 wins, player 2 hawk')
                    else: #player 2 wins
                        node2.fitness += self.payoff_matrix[0]
                        node1.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 0)
                        node2.add_memory(node1.size, 1)
                        #print('player 2 wins, both hawk')
                else: #player 2 plays ignorant dove
                    node1.fitness += self.payoff_matrix[2]
                    node2.fitness += self.payoff_matrix[3]
                    node1.add_memory(node2.size, None)
                    node2.add_memory(node1.size, None)
                    #print('player 1 hawk, player 2 dove')
                    
        elif node2.size > node1.max_size: #player 1 plays dove
            if node1.size < node2.min_size: #player 2 plays hawk
                node2.fitness += self.payoff_matrix[2]
                node1.fitness += self.payoff_matrix[3]
                #print('player 2 hawk, player 1 dove')
            elif node1.size > node2.max_size: #player 2 plays dove
                node1.fitness += self.payoff_matrix[4]
                node2.fitness += self.payoff_matrix[4] 
                #print('both play dove')
            else: #player 2 ignorant
                if node2.aggression > rand_nums[1]: #player 2 plays ignorant hawk
                    node2.fitness += self.payoff_matrix[2]
                    node1.fitness += self.payoff_matrix[3]
                    #print('player 2 hawk, player 1 dove')
                else: #player 2 plays ignorant dove
                    node1.fitness += self.payoff_matrix[4]
                    node2.fitness += self.payoff_matrix[4]
                    #print('both play dove')
            node1.add_memory(node2.size, None)
            node2.add_memory(node1.size, None)
            
        else: #player 1 ignorant
            if node1.aggression > rand_nums[0]: #player 1 plays ignorant hawk
                if node1.size < node2.min_size: #player 2 plays hawk
                    if node1.size > node2.size: #player 1 wins
                        node1.fitness += self.payoff_matrix[0]
                        node2.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 1)
                        node2.add_memory(node1.size, 0)
                        #print('player 2 hawk, player 1 wins')
                    else: #player 2 wins
                        node2.fitness += self.payoff_matrix[0]
                        node1.fitness += self.payoff_matrix[1]
                        node1.add_memory(node2.size, 0)
                        node2.add_memory(node1.size, 1)
                        #print('player 1 hawk, player 2 wins')
                elif node1.size > node2.max_size: #player 2 plays dove
                    node1.fitness += self.payoff_matrix[2]
                    node2.fitness += self.payoff_matrix[3]
                    node1.add_memory(node2.size, None)
                    node2.add_memory(node1.size, None)
                    #print('player 1 hawk, player 2 dove')
                else: #player 2 ignorant
                    if node2.aggression > rand_nums[1]: #player 2 plays ignorant hawk
                        if node1.size > node2.size: #player 1 wins
                            node1.fitness += self.payoff_matrix[0]
                            node2.fitness += self.payoff_matrix[1]
                            node1.add_memory(node2.size, 1)
                            node2.add_memory(node1.size, 0)
                            #print('player 2 hawk, player 1 wins')
                        else: #player 2 wins
                            node2.fitness += self.payoff_matrix[0]
                            node1.fitness += self.payoff_matrix[1]
                            node1.add_memory(node2.size, 0)
                            node2.add_memory(node1.size, 1)
                            #print('player 1 hawk, player 2 wins')
                    else: #player 2 plays ignorant dove
                        node1.fitness += self.payoff_matrix[2]
                        node2.fitness += self.payoff_matrix[3]
                        node1.add_memory(node2.size, None)
                        node2.add_memory(node1.size, None)
                        #print('player 1 hawk, player 2 dove')
            else: #player 1 plays ignorant dove
                if node1.size < node2.min_size: #player 2 plays hawk
                    node2.fitness += self.payoff_matrix[2]
                    node1.fitness += self.payoff_matrix[3]
                    #print('player 2 hawk, player 1 dove')
                elif node1.size > node2.max_size: #player 2 plays dove
                    node1.fitness += self.payoff_matrix[4]
                    node2.fitness += self.payoff_matrix[4]
                    #print('both play dove')
                else: #player 2 ignorant
                    if node2.aggression > rand_nums[1]: #player 2 plays ignorant hawk
                        node2.fitness += self.payoff_matrix[2]
                        node1.fitness += self.payoff_matrix[3]
                        #print('player 2 hawk, player 1 dove')
                    else: #player 2 plays ignorant dove
                        node1.fitness += self.payoff_matrix[4]
                        node2.fitness += self.payoff_matrix[4]
                        #print('both play dove')
                node1.add_memory(node2.size, None)
                node2.add_memory(node1.size, None)

        #Fitness cannot be negative
        if node1.fitness < 0:
            node1.fitness = 0
        if node2.fitness < 0:
            node2.fitness = 0        
        return
    
    def refresh_network(self):
        self.memory_history = [] # memorizes only one generation
        self.fitness_history = []

        if (self.network_methode[0] == 'M1' or self.network_methode[0] == 'M2'):
            self.graphs.append(nx.MultiGraph()) #graph for the new generation
        
        elif (self.network_methode[0] == 'M3'):
            if (self.network_methode[1] == 'Erdos-Renyi'):
                self.graphs.append(nx.gnm_random_graph(self.num_nodes, self.Max_edges))
            if (self.network_methode[1] == 'Small-world'):
                self.graphs.append(nx.watts_strogatz_graph(self.num_nodes, self.network_methode[2], self.network_methode[3]))


        #create new Nodes to fully replace the existing network
        fitness = np.array([node.fitness for node in self.nodes]) #get fitness of Nodes
        mean_fitness = np.mean(fitness)
        fitness = fitness/np.sum(fitness) #fitness values are now normalized
        reproducing_node_index = np.random.choice(self.num_nodes, self.num_nodes, p = fitness) #random weighted choice based on fitness, select num_nodes nodes each having a probability egal to the normalized fitness
        reproducing_node_memory = np.array([len(self.nodes[index].size_memory) for index in reproducing_node_index]) #memory of new nodes is same as parent
        reproducing_node_aggression = np.array([self.nodes[index].aggression for index in reproducing_node_index]) #aggression of new nodes, same as parent

        #record means to see results
        self.history.append([mean_fitness, np.mean(reproducing_node_memory), np.mean(reproducing_node_aggression)])
        
        #add mutations
        memory_mutations = np.random.standard_normal(self.num_nodes).astype(int) #mutation offsets for memory, integers from Gaussian(0,1)
        aggression_mutations = np.random.normal(0, 0.01, self.num_nodes).astype('float64') #mutation offsets for aggression, Gaussian(0, 0.05) values
        reproducing_node_memory += memory_mutations #mutate memory
        reproducing_node_aggression += aggression_mutations #mutate aggression
        
        #sizes = np.random.random_sample(self.num_nodes) #generate uniform sample of sizes
        
        del self.nodes[:] #clear current nodes
        for i in range(self.num_nodes): #create new nodes
            if (self.network_methode[0] != 'M3'):
                self.graphs[len(self.graphs)-1].add_node(i,key=i) 
            #self.nodes.append(Node(sizes[i], reproducing_node_memory[i], reproducing_node_aggression[i]))
            self.nodes.append(Node(i/(self.num_nodes-1), reproducing_node_memory[i], reproducing_node_aggression[i])) #the size is: i/(self.num_nodes-1)
            self.fitness_history.append([self.nodes[i].fitness]) #fill the initial fitness of each fish (0)
            self.memory_history.append([self.nodes[i].max_size-self.nodes[i].min_size])
        
    def show(self):
        ##shows the graph of the last generation
        print(nx.info(self.graphs[len(self.graphs)-1]))
        nx.draw(self.graphs[len(self.graphs)-1],with_labels=True)
        plt.show()