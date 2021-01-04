from class_network import Network
from plots import plot1, plot2, plot_boxes

#Simulation parameters        
num_nodes = 6
interactions_per_node = 2000
hawk_dove_payoff = [0.5, -1.5, 1, 0, 0.5, 0.5]
memory_cost = 0.01  
initial_memory_poisson = 4
initial_aggression = 1
network_methode = ['M3', 'Erdos-Renyi', 4]
#network_methode = ['M2','Uniform',6 , 0.1]
# #Create the initial Network
my_network = Network(num_nodes, interactions_per_node, hawk_dove_payoff, memory_cost, initial_memory_poisson, initial_aggression, network_methode)
my_network.interact()
my_network.show()

plot1(my_network,1)