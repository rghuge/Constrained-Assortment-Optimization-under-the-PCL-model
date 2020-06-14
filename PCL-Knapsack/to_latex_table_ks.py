#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:19:27 2020

@author: rohanghuge
"""

import csv

results_ks_I = []
results_ks_C = []

with open('final_knapsack_I.csv', 'rb') as f:
    reader = csv.reader(f)
    results_ks_I = list(reader)
    

with open('final_knapsack_C.csv', 'rb') as f:
    reader = csv.reader(f)
    results_ks_C = list(reader)
    
    
for i in range(1, 49):
    entry = results_ks_I[i]
    s = '$(' + entry[0] + ', ' + entry[1] + ', ' + entry[2] + ', ' + entry[3] + ', ' + entry[4] + ')$ & ' 
    s = s + str(round(float(entry[5]),2)) + ' & ' + str(round(float(entry[6]),2)) + ' & ' + str(round(float(entry[7]),2)) + ' & ' 
    s = s + str(round(float(entry[8]),2)) + ' & ' + str(round(float(entry[9]),2)) + ' & ' + str(round(float(entry[10]),2)) + '\\\\'
    print(s)
    
for i in range(1, 49):
    entry = results_ks_C[i]
    s = '$(' + entry[0] + ', ' + entry[1] + ', ' + entry[2] + ', ' + entry[3] + ', ' + entry[4] + ')$ & ' 
    s = s + str(round(float(entry[5]),2)) + ' & ' + str(round(float(entry[6]),2)) + ' & ' + str(round(float(entry[7]),2)) + ' & ' 
    s = s + str(round(float(entry[8]),2)) + ' & ' + str(round(float(entry[9]),2)) + ' & ' + str(round(float(entry[10]),2)) + '\\\\'
    print(s)