from class_network import Network
from plots import plot1, plot2, plot_boxes

#Simulation parameters        
num_nodes = 10
interactions_per_node = 2000
hawk_dove_payoff = [0.5, -1.5, 1, 0, 0.5, 0.5]
memory_cost = 0.01  
initial_memory_poisson = 4
initial_aggression = 1
network_methode = ['M3', 'Small-world',4,0]
#network_methode = ['M2','Uniform',6 , 0.1]
# #Create the initial Network
my_network = Network(num_nodes, interactions_per_node, hawk_dove_payoff, memory_cost, initial_memory_poisson, initial_aggression, network_methode)
my_network.interact()
my_network.show()
for i in range(1000): #simulate this many generations
    my_network.interact()
    my_network.refresh_network()
    
t = len(my_network.history)

fitness_history = [my_network.history[i][0] for i in range(t)]
memory_history = [my_network.history[i][1] for i in range(t)]
aggression_history = [my_network.history[i][2] for i in range(t)]
x = np.arange(t)
fig, axes = plt.subplots(3,1, figsize = (20, 15))
axes[0].plot(x, fitness_history)
axes[0].set_title('fitness')
axes[1].plot(x, memory_history)
axes[1].set_title('memory')
axes[2].plot(x, aggression_history)
axes[2].set_title('aggression')
plt.show()


# 2nd graph results of simulation
# all_memory_history=[my_network.memory_history[i] for i in range (0,t,200)] #we memory/ agression / fitness for every time step of 200
# all_aggression_history=[my_network.aggression_history[i] for i in range (0,t,200)]
# all_fitness_history=[my_network.fitness_history[i] for i in range (0,t,200)]

all_memory_history=my_network.memory_history[t-200:t-1] #we memory/ agression / fitness for last time step of 200
all_aggression_history=my_network.aggression_history[t-200:t-1]
all_fitness_history=my_network.fitness_history[t-200:t-1]

fig, ax = plt.subplots()
fig.set_size_inches(13, 10)
ax.set_xlabel('Agression')
ax.set_ylabel('Memory')
ax.set_title('Relationship Between Memory and Agression on the fish')
plt.scatter( all_aggression_history , all_memory_history, c = all_fitness_history, cmap = 'RdPu', alpha =0.5)
cbar = plt.colorbar()
cbar.set_label('Fitness')

# plot memory and fitness according to the generation
pace = 20

fig2, ax2 = plt.subplots()
fig2.set_size_inches(13, 10)
ax2.set_xlabel('Generations')
ax2.set_ylabel('Memory')
ax2.set_title('Relationship Between Memory and Fitness between the generations')
all_generations_history = []
all_fitness_history=my_network.fitness_history[0:t:pace]
all_memory_history=my_network.memory_history[0:t:pace]
for i in range(0,t,pace):
    all_generations_history.append([i]*my_network.num_nodes)
plt.scatter( all_generations_history , all_memory_history, c = all_fitness_history, cmap = 'RdPu', alpha =1)   
cbar = plt.colorbar()
cbar.set_label('Fitness')
plot1(my_network,1)