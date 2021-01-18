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


#Simulation parameters        
num_nodes = 6
interactions_per_node = 2000
hawk_dove_payoff = [0.5, -1.5, 1, 0, 0.5, 0.5]
memory_cost = 0.01  
initial_memory_poisson = 4
initial_aggression = 1
network_methode = ['M1']
#network_methode = ['M3', 'Small-world',4,0]
#network_methode = ['M2','Uniform',6 , 0.1]

#Create the initial Network
my_network = Network(num_nodes, interactions_per_node, hawk_dove_payoff, memory_cost, initial_memory_poisson, initial_aggression, network_methode)
Memory = [] #list of lists (L2) L2 is the list of memory of each individual (in order) at the end. Memory lists L2 for each generation
Fitness = [] #same as Memory but with fitness data
for i in range(4): #simulate this many generations
    my_network.interact()
    Memory.append(lasts(my_network.memory_history))
    Fitness.append(lasts(my_network.fitness_history))
    plot1(my_network,1)
    #plot_transit(my_network,4)
    my_network.refresh_network()
    
print(Memory)