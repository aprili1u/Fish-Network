import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def count_occurrence(list_of_list):  
    ## returns a list of int that corresponds to the number of occurence of each element in each list in list of list
    occurrence=[]
    for L in list_of_list:
        for i in L:
            occurrence.append(L.count(i)) 
    return occurrence

def cercle(r1,r2):
    x = [0] + np.cos(np.linspace(2 * np.pi * r1, 2 * np.pi * r2, 10)).tolist()
    y = [0] + np.sin(np.linspace(2 * np.pi * r1, 2 * np.pi * r2, 10)).tolist()
    xy = np.column_stack([x, y])
    return xy

def plot1(network, pace):
    #plot relationship between fitness and memory for each individual of one generation 
    # the size of the dots depends on the numbers of times that the individual is in that situation
    #returns the Fitness maximum
    l=len(network.memo_uncertainty_history)
    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(13, 10)
    ax2.set_xlabel('individual')
    ax2.set_ylabel('SL-SW')
    ax2.set_title('Relationship Between Individual and Memory for one generation')

    Fitness = []
    Memory = []
    Individual = []
    size = []
    
    fitness_history = network.fitness_history
    memo_uncertainty_history = network.memo_uncertainty_history
    size = count_occurrence(memo_uncertainty_history)
    for i in range(0,l,pace):
        Fitness += fitness_history[i]
        Memory += memo_uncertainty_history[i]
        Individual += [i]*len(memo_uncertainty_history[i])
    plt.scatter(Individual , Memory , s=size, c=Fitness, cmap = 'rainbow', alpha =0.8)
    cbar = plt.colorbar()
    cbar.set_label('Fitness')
    return(max(Fitness))

def plot2(network,Fit_max):
    #same as plot1 but the dots are pie chart where we can visualize 4 categories of fitness
    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(23, 20)
    ax2.set_xlabel('individual')
    ax2.set_ylabel('SL-SW')
    ax2.set_title('Relationship Between Individual and Memory')

    Fitness = []
    Memory = []
    Individual = []
    fitness_history = network.fitness_history
    memo_uncertainty_history = network.memo_uncertainty_history
    size=count_occurrence(memo_uncertainty_history)
    for i in range(len(fitness_history)): # for each individual
        size = count_occurrence([memo_uncertainty_history[i]])
        memo = memo_uncertainty_history[i][0]
        cat = 0
        cat1 = 0 #count occurence (0,Fit_max/4)
        cat2 = 0 #count occurence (Fit_max/4, Fit_max/2)
        cat3 = 0
        cat4 = 0
        for k in range (len(fitness_history[i])):
            fit = fitness_history[i][k]       
            if memo != memo_uncertainty_history[i][k]:            
              #size = cat
                if cat != 0:
                    ax2.scatter(i, memo, s = cat , marker = cercle((cat3+cat2+cat1)/cat,1), facecolor='red') #cat4
                    ax2.scatter(i, memo, s = cat , marker = cercle((cat2+cat1)/cat,(cat3+cat2+cat1)/cat), facecolor='orange')
                    ax2.scatter(i, memo, s = cat , marker = cercle((cat1)/cat,(cat2+cat1)/cat), facecolor='blue')
                    ax2.scatter(i, memo, s = cat , marker = cercle(0,(cat1)/cat), facecolor='purple')
                memo = memo_uncertainty_history[i][k]
                cat = 0
                cat1 = 0
                cat2 = 0
                cat3 = 0
                cat4 = 0
            if fit >= 0 and fit <= Fit_max/4:
                cat1 += 1
            if fit > Fit_max/4 and fit <= Fit_max/2:
                cat2 += 1
            if fit > Fit_max/2 and fit <= Fit_max*3/4:
                cat3 += 1
            if fit > Fit_max*3/4 and fit <= Fit_max:
                cat4 +=1
            cat = cat1 + cat2 + cat3 + cat4 
        if cat != 0:
            ax2.scatter(i, memo,  s = cat, marker = cercle((cat3+cat2+cat1)/cat,1), facecolor='red') #cat4
            ax2.scatter(i, memo,  s = cat, marker = cercle((cat2+cat1)/cat,(cat3+cat2+cat1)/cat), facecolor='orange') #cat 3
            ax2.scatter(i, memo,  s = cat, marker = cercle((cat1)/cat,(cat2+cat1)/cat), facecolor='blue') 
            ax2.scatter(i, memo,  s = cat, marker = cercle(0,(cat1)/cat), facecolor='purple')

    plt.show()

def plot_boxes(network):
    # same as plot1 but with boxes to show Q1,Q2,Q3,Q4
    data = memo_uncertainty_history = network.memo_uncertainty_history
    fig = plt.figure(figsize =(10, 7)) 
    plt.xlabel('Individual')  
    plt.ylabel('SL-SW')  
    plt.title("Box plot of SL-SW") 
    ax = fig.add_axes([0, 0, 1, 1]) 
    bp = ax.boxplot(data) 
    plt.show() 
    
def plot_means(network):
    #plots average fitness, memory, agression for each generation
    t = len(network.history)
    fit_history = [network.history[i][0] for i in range(t)]
    memo_history = [network.history[i][1] for i in range(t)]
    aggr_history = [network.history[i][2] for i in range(t)]
    x = np.arange(t)
    fig, axes = plt.subplots(3,1, figsize = (20, 15))
    axes[0].plot(x, fit_history)
    axes[0].set_title('fitness')
    axes[1].plot(x, memo_history)
    axes[1].set_title('memory')
    axes[2].plot(x, aggr_history)
    axes[2].set_title('aggression')
    plt.show()

def plot_transit(network,indiv):
    # plots a graph of probability of transit from state to state for one individual of one generation
    # the nodes are the different states and the edges the probability of transit -p--->
    
    #nodes = count_occurrence([network.memo_uncertainty_history[indiv]]) #the different states
    dic = {}
    for i in range (len(network.memo_uncertainty_history[indiv])-1):
        edge = (str(round(network.memo_uncertainty_history[indiv][i],2)),str(round(network.memo_uncertainty_history[indiv][i+1],2))) 
        if edge in dic:
            dic[edge] += 1
        else:
            dic[edge] = 1

    edges = [*dic.keys()]
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    plt.figure()    
    prop_width=np.array([*dic.values()]) #can be used for width
    prop_width=prop_width/np.mean(prop_width)
    nx.draw(G,pos,edge_color='black',width=prop_width,linewidths=1,\
    node_size=500,node_color='pink',alpha=0.9,\
    labels={node:node for node in G.nodes()})
    nx.draw_networkx_edge_labels(G,pos,edge_labels=dic,alpha=0.7, label_pos=0.8,font_color='red')
    plt.axis('off')
    plt.show()
    return dic