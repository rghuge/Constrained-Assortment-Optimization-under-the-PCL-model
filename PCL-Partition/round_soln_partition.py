#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:31:52 2020

@author: rohanghuge
"""

from is_feasible import is_feasible

def round_soln_partition(n, x, weight_mat, capacity, partition):
    
    x_hat = greedy(n, x, weight_mat, capacity, partition) # solution from local search starting at x
    
    x_dash = [0]*(n) # another vector to start local search at
    init = -1 # find best node not selected in x_hat
    val = 0
    for i in range(n-1):
        if x_hat[i] != 1:
            val1 = sum([weight_mat[i][j] for j in range(n)])
            if val1 > val:
                val = val1
                init = i
    x_dash[init] = 1   
    x_hat2 = greedy(n, x_dash, weight_mat, capacity, partition)
    
    obj1 = sum([weight_mat[a][b] * x_hat[a] * (1-x_hat[b]) for a in range(n) for b in range(n)]) 
    obj2 = sum([weight_mat[a][b] * x_hat2[a] * (1-x_hat2[b]) for a in range(n) for b in range(n)]) 
    
    if obj1 > obj2:
        return x_hat
    else:
        return x_hat2

################################################################################################

def greedy(n, x, weight_mat, capacity, partition):
        
    og_val = sum([weight_mat[a][b] * x[a] * (1-x[b]) for a in range(n) for b in range(n)]) 
    x_final = list(x)
    improve_by_amt = 0.01/(50**4)
    
    
    x_temp = list(x_final)
    
    # first check delete operations; never want to consider vertex n as it's the dummy vertex
    for i in range(n-1):
        if (x_temp[i] == 1):
            x_temp[i] = 0
            if (is_feasible(x_temp, capacity, partition)):
                val2 = og_val
                for k in range(n):
                    if (k != i and x_temp[k] == 1):
                        val2 = val2 + weight_mat[k][i]
                    
                for k in range(n):
                    if (k != i and x_temp[k] == 0):
                        val2 = val2 - weight_mat[i][k]
                
                if (val2 >= (1+improve_by_amt)*og_val):
                    x_final = list(x_temp)
                    og_val = val2
                    x_temp = list(x_final)
                    continue
            x_temp[i] = 1
            
    
    # next check add operations; never want to consider vertex n as it's the dummy vertex
    for i in range(n-1):
        if (x_temp[i] == 0):
            x_temp[i] = 1
            if (is_feasible(x_temp, capacity, partition)):
                val2 = og_val
                for k in range(n):
                    if (k!= i and x_temp[k] == 0):
                        val2 = val2 + weight_mat[i][k]
                
                for k in range(n):
                    if (k!= i and x_temp[k] == 1):
                        val2 = val2 - weight_mat[k][i]
                
                if (val2 >= (1+improve_by_amt)*og_val):
                    x_final = list(x_temp)
                    og_val = val2
                    x_temp = list(x_final)
                    continue
            x_temp[i] = 0
            
        
    flag = 0

    # finally check for swaps; never want to consider vertex n as it's the dummy vertex
    for i in range(n-1):
        for j in range(n-1):
            if (x_temp[i] == 1 and x_temp[j] == 0):
                x_temp[i] = 0
                x_temp[j] = 1
                if (is_feasible(x_temp, capacity, partition)):
                    val2 = og_val
                    for k in range(n):
                        if (x_temp[k] == 1 and k!=i and k!=j):
                            val2 = val2 - weight_mat[k][j] + weight_mat[k][i]
                            
                    for k in range(n):
                        if (x_temp[k] == 0 and k!=i and k!=j):
                            val2 = val2 + weight_mat[j][k] - weight_mat[i][k]
                    
                    val2 = val2 + weight_mat[j][i] - weight_mat[i][j]
                    
                    if (val2 >= (1+improve_by_amt)*og_val):
                        x_final = list(x_temp)
                        og_val = val2
                        x_temp = list(x_final)
                        flag = 1 # if improving swap found; then restart local search after all swaps considered
                        continue
                x_temp[i] = 1
                x_temp[j] = 0
    
    if (flag == 1):
        return greedy(n, x_final, weight_mat, capacity, partition)
    
    return x_final