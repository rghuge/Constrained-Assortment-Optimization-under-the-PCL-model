#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:23:19 2020

@author: rohanghuge
"""

import numpy as np
import csv
from generate_and_solve_instance_partition import generate_and_solve_instance_partition

ratios = [101]*100

instance_type = [0, 1]
num_products = [50, 100]
gammas = [0.1, 0.5, 1.0]
P0s = [0.25, 0.75]
capacities = [0.4, 0.8]
groups = [3, 7]
delta = 0.001

final_table = [['T', 'n', '\gamma', 'P0', 'd', 'num-parts', 'Avg', 'Min', '5th', '95th', 'Std Dev.', 'CPU Secs']]
for inst_type in instance_type:
    for n in num_products:
        for gamma in gammas:
            for P0 in P0s:
                for capacity in capacities:
                    for num_partitions in groups:
                        soln = generate_and_solve_instance_partition(gamma, P0, inst_type, n, capacity, num_partitions, delta)
                        entry = [];
                        if inst_type == 0:
                            entry.append('I')
                        else:
                            entry.append('C')
                        entry = entry + [n, gamma, P0, capacity, num_partitions]
                        ratios = np.sort(np.array(soln)[:,2])
                        entry.append(np.average(ratios))
                        entry.append(ratios[0])
                        entry.append(ratios[int(0.04 * len(ratios))])
                        entry.append(ratios[int(0.94 * len(ratios))])
                        entry.append(np.std(ratios, axis = 0))
                        entry.append(np.average(np.array(soln)[:,3]))
                        final_table.append(entry)            
            
with open('final_partition_C.csv', 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(final_table)           
