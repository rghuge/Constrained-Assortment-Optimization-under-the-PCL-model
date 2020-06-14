#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:15:05 2020

@author: rohanghuge
"""

import numpy as np

def reduction(n, pref_weight, revenue, gammas):
   
    weight_mat = np.zeros((n + 1, n + 1, 2)) # Define weight matrix where each entry w_ij(z) = [c1, c2]
    V = [[(pref_weight[i] ** (1/gammas[i][j]) + pref_weight[j] ** (1/gammas[i][j])) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # loop until nth node (not n+1)
    for i in range(n):
        for j in range(n) :
            if (i != j) : 
                if V[i][j] != 0:
                    c_ij1 = (pref_weight[i] ** (1/gammas[i][j])) / (V[i][j] ** (1-gammas[i][j]))
                    c_ji1 = (pref_weight[j] ** (1/gammas[i][j])) / (V[i][j] ** (1-gammas[i][j]))
                else:
                    c_ij1 = 0
                    c_ji1 = 0
                
                # set matrix tuple entry for all (i, j) pairs i != j
                weight_mat[i][j][0] = weight_mat[i][j][0] + pref_weight[i]*revenue[i] - c_ij1*revenue[i] 
                weight_mat[i][j][1] = weight_mat[i][j][1] + pref_weight[i] - c_ij1            
                
                weight_mat[j][i][0] = weight_mat[j][i][0] + pref_weight[j]*revenue[j] - c_ji1 * revenue[j]
                weight_mat[j][i][1] = weight_mat[j][i][1] + pref_weight[j] - c_ji1           
                
                
                # set matrix tuple entry for (i, n + 1)
                weight_mat[i][n][0] = weight_mat[i][n][0] + c_ij1 * revenue[i]
                weight_mat[i][n][1] = weight_mat[i][n][1] + c_ij1
                
                weight_mat[j][n][0] = weight_mat[j][n][0] + c_ji1 * revenue[j]
                weight_mat[j][n][1] = weight_mat[j][n][1] + c_ji1

    return weight_mat