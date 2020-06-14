#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 13:17:38 2020

@author: rohanghuge
"""

from gurobipy import GRB
from gurobipy import Model
from gurobipy import quicksum

def maxcut_lp(adj_mat, capacity):
    
    # ensure that we have a square matrix as input 
    if (adj_mat.shape[0]!= adj_mat.shape[1]):
        print("Invalid input. Matrix dimensions don't match!")
        return
    
    # get the number of vertices
    n = adj_mat.shape[0]
    
    # create an empty model
    m = Model()
    m.setParam("OutputFlag", 0);
    
    # create binary decision variables for each vertex
    vertices = []
    for i in range(n):
        vertices.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=str(i)))
    
    # create binary decision variables for each edge
    edges = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name='('+str(i) + ',' + str(j) + ')'))
        edges.append(row)
        
    # since we are done adding varibles, we will update the model
    m.update()
    
    # the objective is to maximize the weight of the cut
    m.setObjective(sum(edges[i][j]*adj_mat[i][j] for i in range(n) for j in range(n)), GRB.MAXIMIZE)
    
    # adding the edge constraints
    for i in range(n):
        for j in range(n):
            m.addConstr(edges[i][j] <= vertices[i], name = '%s_%s_constraint1'%(i, j))
            m.addConstr(edges[i][j] <= (1-vertices[j]), name = '%s_%s_constraint2'%(i, j))
            
    # adding the capacity constraint
    m.addConstr(quicksum(vertices[i] for i in range(n)) <= capacity, name = 'constraint3')
    
    # adding constraint to ensure that the "dummy" vertex is never in our cut
    m.addConstr(vertices[n-1] == 0, name = 'constraint4')
    
    # solve the LP
    m.optimize()
    
    # return the model
    return m
