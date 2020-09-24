# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:59:44 2020

@author: Cécile.A
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
from sympy import symbols,solve,Eq
from scipy.special import factorial
from scipy.stats import skew
from scipy.stats import truncnorm

class Network:
    def __init__(self,nbr_nodes,edge_density):
        self.size=nbr_nodes
        self.edge_density=edge_density
        self.graph=nx.MultiGraph()
        self.nbr_possible_edges=self.size*(self.size-1)/2 
        self.expected_nbr_of_edges=self.edge_density*self.size*(self.size-1)
        self.each_node_nbr_edges=[]
        self.nbr_of_edges=0
        
        ##generate nodes        
        for i in range(self.size):
            self.graph.add_node(i,key=i)
            
    
    def show(self):
        print(nx.info(self.graph))
        nx.draw(self.graph,with_labels=True)
        plt.show()
        return (0)
    
    def set_nbr_of_edges(self,mode=True,para=None):        
        """for each node use distribution to determine nbr of edges it is connected to cf all_deg_centralities
        for mode=='Poisson', no para is needed the variance and the expectency are egal tothe edge_density
        for mode=='uniform', para is the variance the expectency is edge_density """
        
        if (mode==True or mode=='Poisson'):
            self.each_node_nbr_edges=s=np.random.poisson(self.edge_density,self.size)
            self.nbr_of_edges=sum(self.each_node_nbr_edges)
        if (mode=='uniform' and para>=0):
            L=self.edge_density-math.sqrt(3*para)
            H=self.edge_density+math.sqrt(3*para)+1
            self.each_node_nbr_edges=[np.random.randint(np.round(L),np.round(H),self.size)]
            print(int(L))
            print(int(H))
            self.nbr_of_edges=np.sum(self.each_node_nbr_edges)
        #to increase changes of making a graphical sequence we rerun the function if self.nbr_of_edges is odd
        if (self.nbr_of_edges%2==1):
            print(self.set_nbr_of_edges(mode,para))
        else: 
            return(self.each_node_nbr_edges,self.nbr_of_edges)
    
    
    
    def centr_skew(self):
        """Calculates the skewdness of the degree centralities"""
        c_skew = skew(self.each_node_nbr_edges)
        return c_skew
        
    def connect(self):
        """Constructs a symmetrical adjacency matrix based on a list with degree centralities"""
        #RQ:if nbr of edges is odd no graph can be created
        
        arr=self.each_node_nbr_edges
        
        List=arr.tolist()
        self.graph = nx.random_degree_sequence_graph(List,seed=None, tries=10) #creates random network graph with given deg. centr.
        adj_mat = nx.to_numpy_matrix(self.graph) #converts network graph to adjacency matrix
        return np.array(adj_mat)