#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 12:53:16 2020

@author: rohanghuge
"""


def expected_revenue_of_assortment(n, x, pref_weight, revenue, gammas, v0):
    
    for i in range(n):
        if (x[i] != 0 and x[i] != 1):
            raise Exception(('x should be integral. x(' + str(i) + ') = ' + str(x[i])))
   
    # V_ij(x) values
    V = [[(x[i] * pref_weight[i] ** (1/gammas[i][j]) + x[j]* pref_weight[j] ** (1/gammas[i][j])) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # R_ij(x) values
    R_num = [[(revenue[i] * x[i] * (pref_weight[i] ** (1/gammas[i][j])) + revenue[j] * x[j]* (pref_weight[j] ** (1/gammas[i][j]))) if i != j else 0 for j in range(n)] for i in range(n)]
    R = [[R_num[i][j] / V[i][j] if (i !=j and V[i][j] != 0) else 0 for j in range(n)] for i in range(n)]
    
    # nest profits
    V_raised = [[V[i][j]**gammas[i][j] if i!=j else 0 for j in range(n)] for i in range(n)]
    denom = v0 + sum([sum(V_raised[i]) for i in range(n)])
    
    pi = [[((V[i][j]**gammas[i][j]) * R[i][j]) if i!= j else 0 for j in range(n)] for i in range(n)]
    
    # return expected revenue
    return sum([sum(pi[i]) for i in range(n)])/denom


