#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:20:37 2020

@author: rohanghuge
"""

import numpy as np

######### Function to find Max Dicut LP solution using pipage rounding ########
def set_x_pipage(n, soln, weight_mat) :
    
    x_hat = []
    delta = 0
    delta_found = False
    
    # Scan through solution x values to find 0 < delta < 1/2
    for i in range(n) :
        if (soln[i] > 0 and soln[i] < 0.5) :
            delta = soln[i]
            delta_found = True
            break
    
    if (delta_found) :
        
        x1_hat = pipage(n, soln, weight_mat)
        
        # Partitioning the vertex set
        v1 = []
        v2 = []
        v3 = []
        v4 = [] 
        x_dash = soln
        
        # Loop through all vars to assign subsets of indices
        for j in range(n) :
            if (soln[j] == delta) :
                v1.append(j)                
            elif (soln[j] == 1 - delta) :
                v2.append(j)                
            elif (soln[j] == 1/2) :
                v3.append(j)     
            elif (soln[j] == 0 or soln[j] == 1) :
                v4.append(j)
        
        for k in v1 :
            x_dash[k] = min(1, delta + (1 - delta) * len(v2) / len(v1))
        for k in v2 :
            x_dash[k] = max(0, (1 - delta) - (1-delta) * len(v1) / len(v2))
            
        x2_hat = pipage(n, x_dash, weight_mat) # apply pipage to new solution
        
        # final solution value
        obj1 = sum([weight_mat[k][l] * x1_hat[k] * (1-x1_hat[l]) for k in range(n) for l in range(n)])  
        obj2 = sum([weight_mat[k][l] * x2_hat[k] * (1-x2_hat[l]) for k in range(n) for l in range(n)])  
        
        if (obj1 > obj2):
            x_hat = x1_hat
        else:
            x_hat = x2_hat
                          
    # Delta not found
    else : 
        x_hat = pipage(n, soln, weight_mat)
                   
    return x_hat

########################################################################################################################

def pipage(n, soln, weight_mat):
        
    x_t = list(soln)
    non_integral = True
    i = -1 
    j = -1
    pair_found = False
        
    while (non_integral):
        non_integral = False
        for a in range(n):
            if (x_t[a] > 0 and x_t[a] < 1):
                for b in range(n): 
                    if (a != b and x_t[b] > 0 and x_t[b] < 1): # If pair is non-integral                 
                        non_integral = True 
                        pair_found = True
                        i = a
                        j = b
                        break
                    
                if pair_found:
                    break
        
        # Set epsilon bounds
        k = min(x_t[i], 1 - x_t[j])
        l = min(1 - x_t[i], x_t[j])
        
        x_t1 = list(x_t)
        x_t2 = list(x_t)
        
        x_t1[i] = x_t[i] - k
        x_t2[i] = x_t[i] + l 
        
        x_t1[j] = x_t[j] + k
        x_t2[j] = x_t[j] - l
                
        obj1 = sum([weight_mat[a][b] * x_t1[a] * (1-x_t1[b]) for a in range(n) for b in range(n)])  
        obj2 = sum([weight_mat[a][b] * x_t2[a] * (1-x_t2[b]) for a in range(n) for b in range(n)])  
        
        if (obj1 > obj2):
            x_t = list(x_t1)
        else:
            x_t = list(x_t2)
            
        
    # check if there is a single fractional variable
    if (sum(x_t) - int(sum(x_t)) != 0):
        ind = np.where(np.array(x_t) != np.array(x_t).round())[0][0]
        x_t1 = list(x_t)
        x_t2 = list(x_t)
        x_t1[ind] = 0; x_t2[ind] = 1
        
        obj1 = sum([weight_mat[a][b] * x_t1[a] * (1-x_t1[b]) for a in range(n) for b in range(n)])  
        obj2 = sum([weight_mat[a][b] * x_t2[a] * (1-x_t2[b]) for a in range(n) for b in range(n)])  
        
        if (obj1 > obj2):
            x_t = list(x_t1)
        else:
            x_t = list(x_t2)
    
    # deals with numerical issues in final solution
    for i in range(n):
        if (x_t[i] < 0.0000001):
            x_t[i] = 0
        if (x_t[i] > 0.9999999):
            x_t[i] = 1

    
    return x_t
