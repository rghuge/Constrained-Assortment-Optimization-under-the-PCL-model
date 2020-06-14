#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:58:28 2020

@author: rohanghuge
"""

import time
import numpy as np
import csv
from gurobipy import Model
from reduction import reduction
from compute_fixed_point import compute_fixed_point
from weight_mat_given_z import weight_mat_given_z
from maxcut_lp import maxcut_lp
from pipage import set_x_pipage
from expected_revenue_of_assortment import expected_revenue_of_assortment
from generate_instance import generate_instance

def generate_and_solve_instance_cap(gamma, P0, instance_type, n, capacity):
    
    soln_list = []
    
    # Filename in form I/C_n_gamma_P0_delta
    option = ''
    if (instance_type == 0) :
        option = 'I'
    else :
        option = 'C'
    
    f = 'CapedResults/' + option + '_' + str(n) + '_' + str(gamma) + '_' + str(P0) + '_' + str(float(capacity)/n) + '_testing.csv'
    
    

    ############ Generate 100 instances for given parameter combo #############

    for i in range(100):     
        [pref_weight, revenue, gammas, v0] =  generate_instance(instance_type, n, gamma, P0)
        m = Model()
        x = []
           
        start = time.time() # TIME START 
        weight_mat = reduction(n, pref_weight, revenue, gammas)
        z_hat = compute_fixed_point(weight_mat, capacity, v0)
        final_weight_mat = weight_mat_given_z(weight_mat, z_hat, n)
        m = maxcut_lp(np.array(final_weight_mat), capacity)
        for j in range(n+1):   
            x.append(m.getVarByName(str(j)).X)   
        x_hat = set_x_pipage(n+1, x, final_weight_mat)
        del x_hat[-1]
        if (sum(x_hat) > capacity):
            print(x_hat)
            raise Exception('x does not satisfy capacity constraint')
        pi_hat = expected_revenue_of_assortment(n, x_hat, pref_weight, revenue, gammas, v0)  
        end = time.time() # TIME END
        
        # For each instance, store pi, z, and Time elapsed for solving max-cut problem
        soln_list.append([pi_hat, z_hat, min(pi_hat / z_hat * 100, 100), end - start])
        
    # Create and write to file with name f
    with open(f, 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(soln_list)
    
    # return this solution so that we can compute the averages
    return soln_list
      