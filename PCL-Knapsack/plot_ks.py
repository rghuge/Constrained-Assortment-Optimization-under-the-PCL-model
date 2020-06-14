#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 09:53:00 2020

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
    


########### plotting bar graphs ##########################

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
rc('text', usetex=True)


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def autolabel_below(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, -15),  # -3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')



########### knapsack plots ################
# (I,50), (I, 100), (C, 50), (C,100) - min values

# Set init to 1 for 0.1, 2 for 0.25, 3 for 0.5, and 4 for 1.0
init = 3

m1 = 0.0
m2 = 0.0
m3 = 0.0
m4 = 0.0

m1_min = 100.0
m2_min = 100.0
m3_min = 100.0
m4_min = 100.0

for i in range(0, 6):
    j = 4*i + init
    m1 = m1 + float(results_ks_I[j][5])
    if m1_min > round(float(results_ks_I[j][6]),2): m1_min = round(float(results_ks_I[j][6]),2)
    
    m2 = m2 + float(results_ks_C[j][5])
    if m2_min > round(float(results_ks_C[j][6]),2): m2_min = round(float(results_ks_C[j][6]),2)

for i in range(6, 12):
    j = 4*i + init
    m3 = m3 + float(results_ks_I[j][5])
    if m3_min > round(float(results_ks_I[j][6]),2): m3_min = round(float(results_ks_I[j][6]),2)
      
    m4 = m4 + float(results_ks_C[j][5])
    if m4_min > round(float(results_ks_I[j][6]),2): m4_min = round(float(results_ks_C[j][6]),2)


labels = ['(I, 50)', '(I, 100)', '(C, 50)', '(C, 100)']
min_means = [round(m1/6,2), round(m2/6,2), round(m3/6,2), round(m4/6,2)]
min_vals = [m1_min, m2_min, m3_min, m4_min]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, min_means, 2*width, label='Our Avg.')
rects3 = ax.bar(x - width/2, min_vals, 2*width, label='Our Min.', fill = False, ls='--')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Worst-case Guarantees')
ax.set_title(r'Guarantees by ($\mathcal{T}$, $n$) for $\eta$ = 0.5')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()



autolabel(rects1)
autolabel_below(rects3)

fig.tight_layout()

plt.ylim([0,130])

plt.show()       
fig.savefig("ks_bar_0.5.pdf",pad_inches=0.1) 
print(m1_min, m2_min, m3_min, m4_min)

