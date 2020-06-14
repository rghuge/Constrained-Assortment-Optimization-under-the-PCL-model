#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:14:15 2020

@author: rohanghuge
"""

import numpy as np

def round_soln(n, soln, weight_mat, sizes, B):
    
    x_hat = []
    delta = 0
    delta_found = False
    
    # Scan through solution x values to find 0 < delta < 1/2
    for i in range(n) :
        if (soln[i] > 0 and soln[i] < 0.5) :
            delta = soln[i]
            delta_found = True
            break
    
    if sum([soln[i] * sizes[i] for i in range(n)]) == B and delta_found:
        
        # Partitioning the vertex set
        v1 = []
        v2 = []
        v3 = []
        v4 = [] 
        x_prime = list(soln)
        
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
            x_prime[k] = min(1, delta + (1 - delta) * sum([sizes[i] for i in v2]) / sum([sizes[i] for i in v1]))
        for k in v2 :
            x_prime[k] = max(0, (1 - delta) - (1-delta) * sum([sizes[i] for i in v1]) / sum([sizes[i] for i in v2]))
            
        obj1 = sum([weight_mat[a][b] * soln[a] * (1-soln[b]) for a in range(n) for b in range(n)])  
        obj2 = sum([weight_mat[a][b] * x_prime[a] * (1-x_prime[b]) for a in range(n) for b in range(n)])  
        
        if obj1 > obj2:
            x_hat = pipage(n, soln, weight_mat, sizes, B)
        else:
            x_hat = pipage(n, x_prime, weight_mat, sizes, B)
        
    else:
        x_hat = pipage(n, soln, weight_mat, sizes, B)
        
        
    # check if there is a single fractional variable
    if (sum(x_hat) - int(sum(x_hat)) != 0):
        ind = np.where(np.array(x_hat) != np.array(x_hat).round())[0][0]
        x_t1 = list(x_hat)
        x_t2 = [0]*n
        x_t1[ind] = 0; x_t2[ind] = 1
        
        obj1 = sum([weight_mat[a][b] * x_t1[a] * (1-x_t1[b]) for a in range(n) for b in range(n)])  
        obj2 = sum([weight_mat[a][b] * x_t2[a] * (1-x_t2[b]) for a in range(n) for b in range(n)])  
        
        if (obj1 > obj2):
            x_hat = list(x_t1)
        else:
            x_hat = list(x_t2)
    
    # deals with numerical issues in final solution
    for i in range(n):
        if (x_hat[i] < 0.0000001):
            x_hat[i] = 0
        if (x_hat[i] > 0.9999999):
            x_hat[i] = 1

    
    return x_hat
    

def pipage(n, soln, weight_mat, sizes, B):
        
    x_t = list(soln)
    non_integral = True
    i = -1 
    j = -1
    pair_found = False
    iter_num = 0
        
    while (non_integral):
        non_integral = False
        
        # raise error for infinite loop due to numerical issues
        iter_num = iter_num + 1
        if (iter_num > 100):
            print(x_t)
            raise Exception('Pipage in infinite loop')
        
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
        
        if not non_integral:
            break
        
        # Set epsilon bounds
        k = -min(x_t[i], sizes[j] * (1 - x_t[j]) / sizes[i])
        l = min(1 - x_t[i], sizes[j] * x_t[j] / sizes[i])
        
        x_t1 = list(x_t)
        x_t2 = list(x_t)
        
        x_t1[i] = round(x_t[i] + k, 2)
        x_t2[i] = round(x_t[i] + l, 2) 
        
        x_t1[j] = round(x_t[j] - (sizes[i] * k/sizes[j]), 2)
        x_t2[j] = round(x_t[j] - (sizes[i] * l/sizes[j]), 2)
                
        obj1 = sum([weight_mat[a][b] * x_t1[a] * (1-x_t1[b]) for a in range(n) for b in range(n)])  
        obj2 = sum([weight_mat[a][b] * x_t2[a] * (1-x_t2[b]) for a in range(n) for b in range(n)])  
        
        if (obj1 > obj2):
            x_t = list(x_t1)
        else:
            x_t = list(x_t2)
    
    return x_t