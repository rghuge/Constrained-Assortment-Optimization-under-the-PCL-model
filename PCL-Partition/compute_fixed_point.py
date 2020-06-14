#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:39:09 2020

@author: rohanghuge
"""

from gurobipy import GRB
from gurobipy import Model
from gurobipy import quicksum
import math

def compute_fixed_point(weight_mat, capacity, v0, partition):
    
    n = weight_mat.shape[0]
    
    # create an empty model
    m_dual = Model()
    m_dual.setParam( 'OutputFlag', False ) 
    
    
    # setting up the decision variables
    alpha = []
    beta = []
    gamma = []
    delta = []
    z = m_dual.addVar(vtype=GRB.CONTINUOUS, name = 'z')
    
    for i in range(n):
        
        gamma.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='gamma_'+str(i)))
        
        row_alpha = []
        row_beta = []
        for j in range(n):
            if i != j:
                row_alpha.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='alpha_'+str(i) + str(j)))
                row_beta.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='beta_'+str(i) + str(j)))
            else:
                row_alpha.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=0, name='alpha_'+str(i) + str(j)))
                row_beta.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=0, name='beta_'+str(i) + str(j)))
        alpha.append(row_alpha)
        beta.append(row_beta)
        
    for k in range(len(partition)-1):
        delta.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='delta_'+str(k)))
    
    capacities = []
    for k in range(len(partition)-1):
        capacities.append(math.floor(capacity*(round(partition[k+1]) - round(partition[k]))))
        
        
    # since we are done adding varibles, we will update the model
    m_dual.update()
    
    # setting the objective
    obj1 = quicksum([beta[i][j] for i in range(n) for j in range(n)])
    obj2 = quicksum([gamma[i] for i in range(n)])
    obj3 = quicksum([delta[i]*capacities[i] for i in range(len(partition)-1)])
    m_dual.setObjective(obj1 + obj2 + obj3, GRB.MINIMIZE)
    
    # adding constraints
    for i in range(n):
        for j in range(n):
            m_dual.addConstr(alpha[i][j] + beta[i][j] + weight_mat[i][j][1]*z >= weight_mat[i][j][0], name = '%s_%s_constraint1'%(i, j))
            
    for k in range(len(partition)-1):
        for i in range(int(round(partition[k])), int(round(partition[k+1]))):
            m_dual.addConstr(-sum(alpha[i][j] for j in range(n)) + sum(beta[j][i] for j in range(n)) + gamma[i] + delta[k] >= 0, name = '%s_constraint2'%(i))
    
    m_dual.addConstr(obj1 + obj2 + obj3, GRB.EQUAL, v0*z)
        
    # solve the dual
    m_dual.optimize()

    return m_dual.getVarByName('z').X
    #return z