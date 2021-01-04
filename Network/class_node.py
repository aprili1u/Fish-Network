import numpy as np
import matplotlib.pyplot as plt
import math

class Node:
    def __init__(self, size, memory_length, aggression):
        self.size = size
        self.num_interactions = 0
        self.fitness = 0.0
        self.min_size = 0.0 #size of the largest fish you have beaten
        self.max_size = 1.0 #size of smallest fish you have lost to you
        
        #check that memory is positive
        if memory_length < 0:
            memory_length = 0
        self.size_memory = [None]*int(memory_length) #memories the size of the opponent
        self.outcome_memory = [None]*int(memory_length) #memories the outcome of the fight (or interaction ???)
        
        #check that aggression is between 0 and 1
        if aggression > 1.0:
            self.aggression = 1.0
        elif aggression < 0.0:
            self.aggression = 0.0
        else: self.aggression = aggression
            
    def add_memory(self, new_size, outcome):
        
        #if outcome is none there was no fight (no Hawk Hawk)
        if len(self.size_memory) == 0:
            return
        
        #Update the Node's perception of the biggest partner it has beaten and smallest partner it has lost to if the new memory
        #changes these values (min, max).
        if self.num_interactions > len(self.size_memory): #memory is full
            self.outcome_memory.append(outcome) #gain memory
            self.size_memory.append(new_size)
            if outcome == 1: #won fight
                if new_size > self.min_size: #check if new memory changes min
                    self.min_size = new_size #set new min
                    self.size_memory.pop(0) #lose memory
                    self.outcome_memory.pop(0)
                elif self.size_memory[0] == self.min_size: #check if losing min memory
                    self.size_memory.pop(0) #lose memory
                    self.outcome_memory.pop(0)
                    #set new min
                    self.min_size = max([self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 1])
                else: #lose memory
                    self.size_memory.pop(0)
                    self.outcome_memory.pop(0)                
            elif outcome == 0: #lost fight
                if new_size < self.max_size:
                    self.max_size = new_size #set new max
                    self.size_memory.pop(0) #lose memory
                    self.outcome_memory.pop(0)
                elif self.size_memory[0] == self.max_size: #check if losing max memory
                    self.size_memory.pop(0) #lose memory
                    self.outcome_memory.pop(0)
                    #set new max
                    self.max_size = min([self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 0])
                else: #lose memory
                    self.size_memory.pop(0)
                    self.outcome_memory.pop(0)                      
            else: #no fight, lose memory
                self.size_memory.pop(0)
                self.outcome_memory.pop(0)
                #recalculte SL nd SW
                if [self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 0] != []:
                    self.max_size = min([self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 0])
                else :
                    self.max_size = 1.0
                if [self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 1] != []:
                    self.min_size = max([self.size_memory[i] for i in range(len(self.outcome_memory)) if self.outcome_memory[i] == 1])
                else:
                    self.min_size = 0.0
        else: #memory is not full
            if outcome == 1: #won fight
                if new_size > self.min_size: #check if new min
                    self.min_size = new_size
            elif outcome == 0: #lost fight
                if new_size < self.max_size: #check if new max
                    self.max_size = new_size                    
            #gain memory
            self.size_memory[self.num_interactions-1] = new_size
            self.outcome_memory[self.num_interactions-1] = outcome
