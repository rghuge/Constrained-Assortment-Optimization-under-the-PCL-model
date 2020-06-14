#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:04:11 2020

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
from round_soln import round_soln
from expected_revenue_of_assortment import expected_revenue_of_assortment
from generate_instance_ks import generate_instance_ks


def generate_and_solve_instance_ks(gamma, P0, instance_type, n, capacity, size):
    
    soln_list = []
    
    # Filename in form I/C_n_gamma_P0_size
    option = ''
    if (instance_type == 0) :
        option = 'I'
    else :
        option = 'C'
    
    f = option + '_' + str(n) + '_' + str(gamma) + '_' + str(P0) + '_' + str(size) + '_testing.csv'
    
    num_binding = 0

    ############ Generate 100 instances for given parameter combo #############
    for i in range(100):
        
        [pref_weight, sizes, revenue, gammas, v0] =  generate_instance_ks(instance_type, n, gamma, P0, size)
        sizes.append(0) # append a size 0 for the dummy vertex
        m = Model()
        x = []
        
        start = time.time() # TIME START 
        weight_mat = reduction(n, pref_weight, revenue, gammas)
        z_hat = compute_fixed_point(weight_mat, capacity, v0, sizes)
        final_weight_mat = weight_mat_given_z(weight_mat, z_hat, n)
        m = maxcut_lp(np.array(final_weight_mat), capacity, sizes)
        x = []
        for j in range(n+1):
            x.append(m.getVarByName(str(j)).X)   
        x_hat = round_soln(n+1, x, final_weight_mat, sizes, capacity)
        del x_hat[-1] # var corresponding to dummy vertex
        if (round(sum([sizes[k]*x_hat[k] for k in range(n)]), 2) > capacity):
            print(x_hat)
            print(sum([sizes[k]*x_hat[k] for k in range(n)]))
            raise Exception('x does not satisfy knapsack constraint')
        pi_hat = expected_revenue_of_assortment(n, x_hat, pref_weight, revenue, gammas, v0)  
        end = time.time() # TIME END
        
        if (round(sum([sizes[k]*x_hat[k] for k in range(n)]), 2) == capacity):
            num_binding = num_binding+1
        
        # For each instance, store pi, z, and Time elapsed for solving max-cut problem
        soln_list.append([pi_hat, z_hat, min(pi_hat / z_hat * 100, 100), end - start])
        
    print(float(num_binding)/100)    
        
    # Create and write to file with name f
    with open(f, 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(soln_list)
    
    # return this solution so that we can compute the averages
    return soln_list
