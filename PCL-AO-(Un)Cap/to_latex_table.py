#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:19:27 2020

@author: rohanghuge
"""

import csv

results_uncons = []
results_cap = []

with open('final_uncapacitated.csv', 'rb') as f:
    reader = csv.reader(f)
    results_uncons = list(reader)
    

with open('final_capacitated.csv', 'rb') as f:
    reader = csv.reader(f)
    results_cap = list(reader)
    

#for i in range(1, len(results_uncons)):
#    entry = results_uncons[i]
#    s = '$(' + entry[0] + ', ' + entry[1] + ', ' + entry[2] + ', ' + entry[3] + ')$ & ' 
#    s = s + str(round(float(entry[5]),2)) + ' & ' + str(round(float(entry[4]),2)) + ' & ' + str(round(float(entry[6]),2)) + ' & ' 
#    s = s + str(round(float(entry[7]),2)) + ' & ' + str(round(float(entry[8]),2)) + ' & ' + str(round(float(entry[9]),2)) + '\\\\'
#    print(s)
    
for i in range(1, len(results_cap)):
    entry = results_cap[i]
    s = '$(' + entry[0] + ', ' + entry[1] + ', ' + entry[2] + ', ' + entry[3] + ', ' + entry[4] + ')$ & ' 
    s = s + str(round(float(entry[6]),2)) + ' & ' + str(round(float(entry[5]),2)) + ' & ' + str(round(float(entry[7]),2)) + ' & ' 
    s = s + str(round(float(entry[8]),2)) + ' & ' + str(round(float(entry[9]),2)) + ' & ' + str(round(float(entry[10]),2)) + '\\\\'
    print(s)