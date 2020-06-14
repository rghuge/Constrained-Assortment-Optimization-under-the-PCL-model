#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:50:58 2020

@author: rohanghuge
"""

import numpy as np
import csv
from generate_and_solve_instance_ks import generate_and_solve_instance_ks

ratios = [101]*100

instance_type = [0, 1]
num_products = [50, 100]
gammas = [0.1, 0.5, 1.0]
P0s = [0.25, 0.75]
sizes = [0.1, 0.25, 0.5, 1.0]
capacity = 1

final_table = [['T', 'n', '\gamma', 'P0', 's', 'Avg', 'Min', '5th', '95th', 'Std Dev.', 'CPU Secs']]
for inst_type in instance_type:
    for n in num_products:
        for gamma in gammas:
            for P0 in P0s:
                for size in sizes:
                    soln = generate_and_solve_instance_ks(gamma, P0, inst_type, n, capacity, size)
                    entry = [];
                    if inst_type == 0:
                        entry.append('I')
                    else:
                        entry.append('C')
                    entry = entry + [n, gamma, P0, size]
                    ratios = np.sort(np.array(soln)[:,2])
                    entry.append(np.average(ratios))
                    entry.append(ratios[0])
                    entry.append(ratios[int(0.04 * len(ratios))])
                    entry.append(ratios[int(0.94 * len(ratios))])
                    entry.append(np.std(ratios, axis = 0))
                    entry.append(np.average(np.array(soln)[:,3]))
                    final_table.append(entry)

with open('final_knapsack.csv', 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(final_table)           
