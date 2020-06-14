#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:13:05 2020

@author: rohanghuge
"""

import numpy as np

independent = 0
correlated = 1

def generate_instance_ks(instance_type, n, gamma, P0, size):

    # generate a vector of random preference weights for the items
    pref_weight = np.random.rand(1,n).tolist()[0]
    
    # generate a vector of random sizes for the items; ensure a minimum size
    sizes = ((0.01 + np.random.rand(1,n)*0.99) * size).tolist()[0]
    
    # based on the instance type we generate a vector of revenues for the items
    if (instance_type == independent) :
        revenue = np.random.rand(1,n).tolist()[0]
    else :
        revenue = (1 - np.array(pref_weight)).tolist()
        
    # we generate a random matrix with elements uniformly distributed in [0,1) 
    # and then multiply it by the given gamma value to scale down the distribution.
    # Next we symmetrize it in a way that keeps the distribition.
    a_random_matrix = np.random.rand(n, n) * gamma
    gammas = a_random_matrix.tolist()
    gammas = (np.tril(a_random_matrix) + np.tril(a_random_matrix, -1).T).tolist()
    
    # compute v0 as in Zhang et. al.
    V_ij = [[(pref_weight[i] ** (1/gammas[i][j]) + pref_weight[j] ** (1/gammas[i][j])) ** gammas[i][j] if i != j else 0 for j in range(n)] for i in range(n)]
    v0 = float(P0 * sum([sum(V_ij[i]) for i in range(n)])) / (1 - P0)
    
    # return the generated vectors as a tuple
    return [pref_weight, sizes, revenue, gammas, v0]
