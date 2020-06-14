#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 08:58:57 2020

@author: rohanghuge
"""

import csv

results_p_I = []
results_p_C = []

with open('final_partition_I.csv', 'rb') as f:
    reader = csv.reader(f)
    results_p_I = list(reader)
    

with open('final_partition_C.csv', 'rb') as f:
    reader = csv.reader(f)
    results_p_C = list(reader)
    
    
for i in range(1, 49):
    entry = results_p_I[i]
    s = '$(' + entry[0] + ', ' + entry[1] + ', ' + entry[2] + ', ' + entry[3] + ', ' + entry[4] + ', ' + entry[5] + ')$ & ' 
    s = s + str(round(float(entry[6]),2)) + ' & ' + str(round(float(entry[7]),2)) + ' & ' + str(round(float(entry[8]),2)) + ' & ' 
    s = s + str(round(float(entry[9]),2)) + ' & ' + str(round(float(entry[10]),2)) + ' & ' + str(round(float(entry[11]),2)) + '\\\\'
    print(s)
    
for i in range(1, 49):
    entry = results_p_C[i]
    s = '$(' + entry[0] + ', ' + entry[1] + ', ' + entry[2] + ', ' + entry[3] + ', ' + entry[4] + ', ' + entry[5] + ')$ & ' 
    s = s + str(round(float(entry[6]),2)) + ' & ' + str(round(float(entry[7]),2)) + ' & ' + str(round(float(entry[8]),2)) + ' & ' 
    s = s + str(round(float(entry[9]),2)) + ' & ' + str(round(float(entry[10]),2)) + ' & ' + str(round(float(entry[11]),2)) + '\\\\'
    print(s)