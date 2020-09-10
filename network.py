# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 15:42:28 2020

@author: Cécile.A
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
from sympy import symbols,solve,Eq
from scipy.special import factorial


class Network:
    
    def __init__(self,nbr_nodes,nbr_edges):
        self.nbr_edges=nbr_edges
        self.nbr_nodes=nbr_nodes
        self.graph=nx.MultiGraph()
        
        self.Max_edges=self.nbr_nodes*(self.nbr_nodes+1)/2
        self.list_id_edges=[]
        ##generate nodes
        for i in range(nbr_nodes):
            self.graph.add_node(i,key=i)
                
        self.id_edges=id_edges(self.Max_edges)

        
    def show(self):
        print(nx.info(self.graph))
        nx.draw(self.graph,with_labels=True)
        plt.show()
        return (0)
    
    def set_edges(self,mode=True,nbr_of_edges=True):
        ##mode is the type of law used to generate the edges is can be:
            ##uniform, poisson, weibull or geometrical, by default it's poisson
            ##we can have multiple times the same edge made  
            ##L is the list of id of edges: 1 is the edge between node 1 and node 0, 2 the edge btw 2 and 0 ; 3 the edge btw 2 and 1 etc... nbres are distributed line by line
        L=[]
        
        ## lambda for the poisson law is egal to nbr_nodes/2 if the out come is higher than nbr_nodes we get a need nbr
        
        if (nbr_of_edges==True):
            nbr=self.nbr_edges
        else:
            nbr=nbr_of_edges
            
        if (mode == True or mode=='Poisson'):
            k=0
            while (k<nbr):
                s=np.random.poisson(self.nbr_nodes/2,1)
                if (s<self.nbr_nodes or s not in L):      ##not in doesn't work here
                    L.append(int(s)) 
                    k+=1
                    
        ## uniform law
        if (mode=='uniform'):
            k=0
            while (k<nbr):
                s=np.random.randint(1,self.Max_edges+1,1)
                if (s not in L): ##not in doesn't work here
                    L.append(int(s))
                    k+=1
            
        ##weibull
        #if (mode=='weibull')
        ##create the edges
        print(L)
        d=self.id_edges
        for i in L:
            self.graph.add_edges_from([d[i]])
        if (nbr_of_edges==True):
            self.list_id_edges=L
        else:
            self.list_id_edges+=L
        return(L)
                
                
    
    def refresh(self,coef,mode=True):
        ###when coef == 0 the graph is not changed when coef== 1 all edges are rerun using set edges
        ###We can decide the mode the edges are added
        
        nbr_of_edge_to_modify=int(coef*len(self.list_id_edges))
        Modify=self.list_id_edges[0:nbr_of_edge_to_modify]
        
        ###first we remove nbr_of_edge_to_modify from the list of edges, starting from the index 0 of the list
        d=self.id_edges
        for i in Modify:
            self.graph.remove_edges_from([d[i]])
            
        ###Than we creat need edges 
        self.set_edges(mode,nbr_of_edge_to_modify)
        return(self.list_id_edges)
        
        
            
   

def id_edges(z):
    ##return a dictionnaire associating to each edge the nodes concerned. 

    d={}
    x=0 
    y=0
    for i in range (1,int(z+1)):
        if(x<y):
            
            d[i]=(y,x)
            x+=1
            
        else:
            y+=1
            x=0
            d[i]=(y,x)
            x+=1
    return(d)               