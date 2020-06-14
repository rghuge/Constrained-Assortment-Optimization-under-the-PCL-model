#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:15:47 2020

@author: rohanghuge
"""

import time
import csv
from generate_instance_partition import generate_instance_partition
from reduction import reduction
from compute_fixed_point import compute_fixed_point
from weight_mat_given_z import weight_mat_given_z
from alg_z import alg_z
from expected_revenue_of_assortment import expected_revenue_of_assortment
from is_feasible import is_feasible
from round_soln_partition import round_soln_partition

def generate_and_solve_instance_partition(gamma, P0, instance_type, n, capacity, num_partitions, delta):
    
    soln_list = []
    
    # Filename in form I/C_n_gamma_P0_cap_numparts
    option = ''
    if (instance_type == 0) :
        option = 'I'
    else :
        option = 'C'
    
    f = 'PartitionResults/' + option + '_' + str(n) + '_' + str(gamma) + '_' + str(P0) + '_' + str(capacity) + '_' + str(num_partitions) + '_testing.csv'

    ############ Generate 100 instances for given parameter combo #############
    for i in range(100):
        [pref_weight, revenue, gammas, v0, partition] =  generate_instance_partition(instance_type, n, gamma, P0, num_partitions)
        partition = [0] + partition + [n]
        
        start = time.time() # TIME START 
        weight_mat = reduction(n, pref_weight, revenue, gammas)
        z_guess =  compute_fixed_point(weight_mat, capacity, v0, partition)   
        L = (pref_weight[0]*revenue[0])/(2*max(pref_weight))
        R = min(max(revenue), z_guess)
        eps = delta * L
        x = [0]*(n+1)
        
        while (R - L > eps):
#            print(R - L, eps)
            z_hat = (R+L)/2
            final_weight_mat = weight_mat_given_z(weight_mat, z_hat, n)
            x_hat = round_soln_partition(n+1, x, final_weight_mat, capacity, partition)
            x = list(x_hat)
            del x_hat[-1] # var corresponding to dummy vertex
            az = alg_z(n, x_hat, pref_weight, revenue, gammas, v0, z_hat)  
            if (az >= v0*z_hat):
                L = z_hat
            else:
                R = z_hat
            
        if (R - L <= eps):
            z_hat = L
            final_weight_mat = weight_mat_given_z(weight_mat, z_hat, n)
            x_hat = round_soln_partition(n+1, x, final_weight_mat, capacity, partition)
            x = list(x_hat)
            del x_hat[-1] # var corresponding to dummy vertex
            if (not is_feasible(x_hat, capacity, partition)):
                print(x_hat)
                raise Exception('x_hat does not satisfy partition constraints')
            pi_hat = expected_revenue_of_assortment(n, x_hat, pref_weight, revenue, gammas, v0) 
        
        end = time.time() # TIME END
        
        # For each instance, store pi, z, and Time elapsed for solving max-cut problem
        soln_list.append([pi_hat, z_guess, min(pi_hat / z_guess * 100, 100), end - start])
#        print(i, end-start)
        
    # Create and write to file with name f
    with open(f, 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(soln_list)
    
    # return this solution so that we can compute the averages
    return soln_list
      