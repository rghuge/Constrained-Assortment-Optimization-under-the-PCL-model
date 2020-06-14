#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:37:13 2020

@author: rohanghuge
"""

import math

def is_feasible(x, capacity, partition):
    for k in range(len(partition)-1):
        if (sum(x[i] for i in range(int(round(partition[k])), int(round(partition[k+1])))) > 
            math.floor(capacity*(round(partition[k+1]) - round(partition[k])))):
            return False
    return True