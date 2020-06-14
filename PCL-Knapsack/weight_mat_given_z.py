#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:16:08 2020

@author: rohanghuge
"""

def weight_mat_given_z(weight_mat, z, n):
    return [[weight_mat[i][j][0] - weight_mat[i][j][1] * z for j in range(n+1)] for i in range(n+1)]