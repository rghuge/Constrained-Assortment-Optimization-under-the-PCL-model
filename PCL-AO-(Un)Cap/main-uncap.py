#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:33:40 2020

@author: rohanghuge
"""

import numpy as np
import csv
from generate_and_solve_instance import generate_and_solve_instance

min_ratio = 100
ratios = [101]*100


################### Generate the 36 different parameter combos ################

instance_type = [0, 1]
num_products = [50, 100]
gammas = [1.0, 0.5, 0.1]
P0s = [0.25, 0.5, 0.75]



final_table = [['T', 'n', '\gamma', 'P0', 'Avg', 'Min', '5th', '95th', 'Std Dev.', 'CPU Secs']]

for inst_type in instance_type:
    for P0 in P0s:
        for gamma in gammas:
            for n in num_products:
                soln = generate_and_solve_instance(gamma, P0, inst_type, n, 10*n)
                entry = [];
                if inst_type == 0:
                    entry.append('I')
                else:
                    entry.append('C')
                entry = entry + [n, gamma, P0]
                ratios = np.sort(np.array(soln)[:,2])
                entry.append(np.average(ratios))
                entry.append(ratios[0])
                entry.append(ratios[4])
                entry.append(ratios[94])
                entry.append(np.std(ratios, axis = 0))
                entry.append(np.average(np.array(soln)[:,3]))
                
                final_table.append(entry)

                                                
            
with open('final_uncapacitated.csv', 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(final_table)           