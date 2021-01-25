from class_network import Network
from plots import plot1, plot2, plot_boxes, plot_means, plot_transit
import numpy as np
import matplotlib.pyplot as plt

def lasts(L):
    """L is a list of lists lasts return a list of last items of each list in L"""
    Lasts = []
    for ind in L: #browse L
        Lasts.append(ind[-1])
    return Lasts

def mean_per_indiv(L):
    """L is a list of lists mean_per_indiv return a list of the average avalue of each list in L"""
    M = []
    for ind in L: #browse L
        M.append(np.mean(ind))
    return M

def combine_dictionnaries(ini_dictionary1,ini_dictionary2):
    # combining dictionaries 
    # using dict comprehension and set 
    final_dictionary =  {x: ini_dictionary1.get(x, 0) + ini_dictionary2.get(x, 0) 
                    for x in set(ini_dictionary1).union(ini_dictionary2)}

    return(final_dictionary) 

#Simulation parameters        
num_nodes = 6
interactions_per_node = 2000
hawk_dove_payoff = [0.5, -1.5, 1, 0, 0.5, 0.5]
memory_cost = 0.01  
initial_memory_poisson = 1
initial_aggression = 1
#network_methode = ['M1']
network_methode = ['M3', 'Small-world',4,0.3]
#network_methode = ['M2','Uniform',6 , 0.1]

#Create the initial Network
my_network = Network(num_nodes, interactions_per_node, hawk_dove_payoff, memory_cost, initial_memory_poisson, initial_aggression, network_methode)
Memo_uncertainty = [] #list of lists (L2) L2 is the list of memory of each individual (in order) at the end. Memory lists L2 for each generation
Fitness = [] #same as Memory but with fitness data
Aggression = []
Memo_size = []
for i in range(4): #simulate this many generations
    my_network.interact()
    Memo_uncertainty.append(mean_per_indiv(my_network.memo_uncertainty_history))
    Fitness.append(lasts(my_network.fitness_history))
    Aggression.append(list(my_network.aggression))
    Memo_size.append(list(my_network.memory))
    #plot1(my_network,1)
    #print(plot_transit(my_network,4))
    my_network.show()
    print(my_network.max_centrality)
    print(my_network.min_centrality)
    
    my_network.refresh_network()
    
#print(Memo_size)
#print(Aggression)