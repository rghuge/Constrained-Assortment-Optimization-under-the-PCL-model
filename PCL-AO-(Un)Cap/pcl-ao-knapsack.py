h #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 17:18:08 2018

@author: RohanGhuge, JoeKwon, AdeteeSharma
"""


# import the required packages
from gurobipy import *
import random 
import numpy as np
import time
import csv

independent = 0
correlated = 1

####################################################################################################################################
def generate_instance(instance_type, n, gamma, P0, size):

    # generate a vector of random preference weights for the items
    pref_weight = np.random.rand(1,n).tolist()[0]
    
    # generate a vector of random sizes for the items
    sizes = (np.random.rand(1,n)*size).tolist()[0]
    
    # based on the instance type we generate a vector of revenues for the items
    if (instance_type == independent) :
        revenue = np.random.rand(1,n).tolist()[0]
    else :
        revenue = (1 - np.array(pref_weight)).tolist()
        
    # we generate a random matrix with elements uniformly distributed in [0,1) 
    # and then multiply it by the given gamma value to scale down the distribution.
    # Next we symmetrize it in a way that keeps the distribition.
    a_random_matrix = np.random.rand(n, n) * gamma
    gammas = a_random_matrix.tolist()
    #gammas = (np.tril(a_random_matrix) + np.tril(a_random_matrix, -1).T).tolist()
    
    # compute v0 as in Zhang et. al.
    V_ij = [[(pref_weight[i] ** (1/gammas[i][j]) + pref_weight[j] ** (1/gammas[i][j])) ** gammas[i][j] if i != j else 0 for j in range(n)] for i in range(n)]
    v0 = float(P0 * sum([sum(V_ij[i]) for i in range(n)])) / (1 - P0)
    
    # return the generated vectors as a tuple
    return [pref_weight, sizes, revenue, gammas, v0]


####################################################################################################################################


def reduction(n, pref_weight, revenue, gammas):
   
    # Define weight matrix where each entry w_ij(z) = [c1, c2]
    weight_mat = np.zeros((n + 1, n + 1, 2))
    
    # V_ij(x) values
    V = [[(pref_weight[i] ** (1/gammas[i][j]) + pref_weight[j] ** (1/gammas[i][j])) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # loop until nth node (not n+1)
    for i in range(n):
        
        # keep sum for arcs (i --> n + 1)
        sum_i1 = 0
        sum_i2 = 0
        
        for j in range(n) :
            if (i != j) : 
                
                if V[i][j] != 0:
                    c_ij1 = (pref_weight[i] ** (1/gammas[i][j])) / (V[i][j] ** (1-gammas[i][j]))
                    c_ji1 = (pref_weight[j] ** (1/gammas[i][j])) / (V[i][j] ** (1-gammas[i][j]))
                else:
                    c_ij1 = 0
                    c_ji1 = 0
                    
                # set matrix tuple entry for all (i, j) pairs i != j
                #print('i:' + str(i) + ', j:' + str(j))
                weight_mat[i][j][0] = weight_mat[i][j][0] + pref_weight[i]*revenue[i] - c_ij1*revenue[i] 
                weight_mat[i][j][1] = weight_mat[i][j][1] + pref_weight[i] - c_ij1            
                
                weight_mat[j][i][0] = weight_mat[j][i][0] + pref_weight[j]*revenue[j] - c_ji1 * revenue[j]
                weight_mat[j][i][1] = weight_mat[j][i][1] + pref_weight[j] - c_ji1           
        
                # set matrix tuple entry for (i, n + 1)
                weight_mat[i][n][0] = weight_mat[i][n][0] + c_ij1 * revenue[i]
                weight_mat[i][n][1] = weight_mat[i][n][1] + c_ij1
                
                weight_mat[j][n][0] = weight_mat[j][n][0] + c_ji1 * revenue[j]
                weight_mat[j][n][1] = weight_mat[j][n][1] + c_ji1

    return weight_mat

####################################################################################################################################

def compute_fixed_point(weight_mat, capacity, v0, sizes):
    
    n = weight_mat.shape[0]
    
    # create an empty model
    m_dual = Model()
    m_dual.setParam( 'OutputFlag', False ) 
    
    
    # setting up the decision variables
    alpha = []
    beta = []
    gamma = []
    delta = m_dual.addVar(vtype = GRB.CONTINUOUS, lb=0, name = 'delta')
    z = m_dual.addVar(vtype=GRB.CONTINUOUS, name = 'z')
    
    for i in range(n):
        
        gamma.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='gamma_'+str(i)))
        
        row_alpha = []
        row_beta = []
        for j in range(n):
             row_alpha.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='alpha_'+str(i) + str(j)))
             row_beta.append(m_dual.addVar(vtype=GRB.CONTINUOUS, lb=0, name='beta_'+str(i) + str(j)))
        alpha.append(row_alpha)
        beta.append(row_beta)
        
    # since we are done adding varibles, we will update the model
    m_dual.update()
    
    # setting the objective
    obj1 = quicksum([beta[i][j] for i in range(n) for j in range(n)])
    obj2 = quicksum([gamma[i] for i in range(n)])
    m_dual.setObjective(obj1 + obj2 + capacity*delta, GRB.MINIMIZE)
    
    # adding constraints
    for i in range(n):
        for j in range(n):
            m_dual.addConstr(alpha[i][j] + beta[i][j] + weight_mat[i][j][1]*z >= weight_mat[i][j][0], name = '%s_%s_constraint1'%(i, j))
            
    for i in range(n):
        m_dual.addConstr(-sum(alpha[i][j] for j in range(n)) + sum(beta[j][i] for j in range(n)) + gamma[i] + sizes[i]*delta >= 0, name = '%s_constraint2'%(i))
    
    m_dual.addConstr(obj1 + obj2 + capacity*delta, GRB.EQUAL, v0*z)
        
    # solve the dual
    m_dual.optimize()

    return m_dual.getVarByName('z').X
    #return z

####################################################################################################################################

def weight_mat_given_z(weight_mat, z, n):
    return [[weight_mat[i][j][0] - weight_mat[i][j][1] * z for j in range(n+1)] for i in range(n+1)]

####################################################################################################################################

def maxcut_lp(adj_mat, capacity, sizes):
    
    # ensure that we have a square matrix as input 
    if (adj_mat.shape[0]!= adj_mat.shape[1]):
        print("Invalid input. Matrix dimensions don't match!")
        return
    
    # get the number of vertices
    n = adj_mat.shape[0]
    
    # create an empty model
    m = Model()
    m.setParam('OutputFlag', False) 
    
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
    m.addConstr(quicksum(sizes[i]*vertices[i] for i in range(n-1)) <= capacity, name = 'constraint3')
    
    # adding constraint to ensure that the "infinity" vertex is never in our cut
    m.addConstr(vertices[n-1] == 0, name = 'constraint4')
    
    # solve the LP
    m.optimize()
    
    # return the model
    return m

####################################################################################################################################

# round solution for max dicut with knapsack const
def round_soln(adj_mat, lp_soln, sizes, B):
    
    n = adj_mat.shape[0]
    x = list(lp_soln)
    
    while (True):
        
        #print (x)
        # check if soln has non-integral values
        count = 0
        for i in range(n):
            if (x[i] != 0 and x[i] != 1):
                count = count + 1
        
        #print('count: ' + str(count))
        
        if count == 0: return x
        
        if count == 1:
            frac_ind = -1
            for i in range(n):
                if (x[i] != 0 and x[i] != 1):
                    frac_ind = i
            
            currentB = sum([x[i] * sizes[i] for i in range(n)])
            #print('here')
            #print(currentB, currentB + (1-x[frac_ind])*sizes[frac_ind], 
                  #currentB - x[frac_ind]*sizes[frac_ind], B)
            
            x_1 = list(x); x_2 = list(x)            
            x_1[frac_ind] = 0; x_2[frac_ind] = 1
            obj = 0; obj1 = 0; obj2 = 0
            w0 = 0; w1 = 0
            
            for a in range(n):
                for b in range(n):
                    obj += adj_mat[a][b] * x[a] * (1 - x[b])
                    obj1 += adj_mat[a][b] * x_1[a] * (1 - x_1[b])
                    obj2 += adj_mat[a][b] * x_2[a] * (1 - x_2[b])
            
            #print(obj, obj1, obj2)            
            if (currentB + (1-x[frac_ind])*sizes[frac_ind] > B):
                x_3 = [0]*n; x_3[frac_ind] = 1
                obj3 = sum([adj_mat[a][b] * x_3[a] * (1 - x_3[b]) for a in range(n) for b in range(n)])
                if obj1 > obj3: return x_1
                else: return x_3
            
            else:
                if obj1 > obj2: return x_1
                else: return x_2
                
            
        if count > 1:
            flag = 0
            for i in range(n):
                '''max1 = 0
                for a in range(n):
                    if x[a] != 0 and x[a] != 1 and sizes[a] > max1:
                        max1 = a
                i = max1'''
                
                for j in range(n):
                    if i == j:
                        continue
                    
                    
                    
                    if (x[i] != 0 and x[i] != 1 and x[j] != 0 and x[j] != 1):
                        x_1 = list(x)
                        x_2 = list(x)
                        
                        l = -min(x[i], sizes[j] * (1 - x[j]) / sizes[i])
                        k = min(1 - x[i], sizes[j] * x[j] / sizes[i])
                        
                        x_1[i] = round(x_1[i] + l, 7)
                        x_1[j] = round(x_1[j] - (sizes[i] * l / sizes[j]), 7)
                        
                        x_2[i] = round(x_2[i] + k, 7)
                        x_2[j] = round(x_2[j] - (sizes[i] * k / sizes[j]), 7)
                        
                        
                        obj1 = 0
                        obj2 = 0
                        
                        for a in range(n):
                            for b in range(n):
                                obj1 += adj_mat[a][b] * x_1[a] * (1 - x_1[b])
                                obj2 += adj_mat[a][b] * x_2[a] * (1 - x_2[b])
                        
                        if obj1 >= obj2:
                            x = list(x_1)
                        else:
                            x = list(x_2)
                        
                        flag = 1
                    if flag == 1:
                        break
                if flag == 1:
                    break
                        
#####################################################################################################

def expected_revenue_of_assortment(n, x, pref_weight, revenue, gammas, v0):
    
    for i in range(n):
        if (x[i] != 0 and x[i] != 1):
            print('###################################################')
            print('###################################################')
            print('###################################################')
            print('###################################################')
            print('###################################################')
            time.sleep(100)
    
    # V_ij(x) values
    V = [[(x[i] * pref_weight[i] ** (1/gammas[i][j]) + x[j]* pref_weight[j] ** (1/gammas[i][j])) if i != j else 0 for j in range(n)] for i in range(n)]
    
    # R_ij(x) values
    R_num = [[(revenue[i] * x[i] * (pref_weight[i] ** (1/gammas[i][j])) + revenue[j] * x[j]* (pref_weight[j] ** (1/gammas[i][j]))) if i != j else 0 for j in range(n)] for i in range(n)]
    R = [[R_num[i][j] / V[i][j] if (i !=j and V[i][j] != 0) else 0 for j in range(n)] for i in range(n)]
    
    # nest profits
    V_raised = [[V[i][j]**gammas[i][j] if i!=j else 0 for j in range(n)] for i in range(n)]
    denom = v0 + sum([sum(V_raised[i]) for i in range(n)])
    
    pi = [[((V[i][j]**gammas[i][j]) * R[i][j]) if i!= j else 0 for j in range(n)] for i in range(n)]
    
    # return expected revenue
    return sum([sum(pi[i]) for i in range(n)])/denom


####################################################################################################################################

def generate_and_solve_instance(gamma, P0, instance_type, n, capacity, size):
    
    soln_list = []
    
    ############################ FILE NAMING ##################################
    type = ''
    if (instance_type == 0) :
        type = 'I'
    else :
        type = 'C'
    
    # Filename in form I/C___n___gamma__P0
    f = type + '_' + str(n) + '_' + str(gamma) + '_' + str(P0) + '_' + str(size) + '_testing.csv'

    ############ Generate 100 instances for given parameter combo #############
    for i in range(100):
        # Generates the parameters
        [pref_weight, sizes, revenue, gammas, v0] =  generate_instance(instance_type, n, gamma, P0, size)
        sizes.append(0)
        
        # TIME START 
        start = time.time()
        
        weight_mat = reduction(n, pref_weight, revenue, gammas)
        z_hat = compute_fixed_point(weight_mat, capacity, v0, sizes)
        final_weight_mat = weight_mat_given_z(weight_mat, z_hat, n)
        m = maxcut_lp(np.array(final_weight_mat), capacity, sizes)
        x = []
        for j in range(n+1):
            x.append(m.getVarByName(str(j)).X)   
        x_hat = round_soln(np.array(final_weight_mat), x, sizes, capacity)
        
        s_1 = 0.0; s_2 = 0.0
        for j in range(n+1):
            if (x[j] == 0 or x[j] == 0.5 or x[j] == 1): 
                continue
            elif (x[j] < 0.5 and x[j] > 0): 
                s_1 += sizes[j]
            else: 
                s_2 += sizes[j]
        
        
        x_2 = [0]*(n+1)
        for j in range(n+1):
            if (x[j] == 0 or x[j] == 0.5 or x[j] == 1): 
                x_2[j] = x[j]
            elif (x[j] < 0.5 and x[j] > 0): 
                #print(x[j])
                x_2[j] = min(1, x[j] + (1-x[j])*s_2/s_1)
            else: 
                x_2[j] = max(0, x[j] - x[j]*s_1/s_2) 
        x_hat2 = round_soln(np.array(final_weight_mat), x_2, sizes, capacity)
        
        obj1 = sum([final_weight_mat[k][l] * x_hat[k] * (1-x_hat[l]) for k in range(n+1) for l in range(n+1)])  
        obj2 = sum([final_weight_mat[k][l] * x_hat2[k] * (1-x_hat2[l]) for k in range(n+1) for l in range(n+1)])  
        
        if (obj2 > obj1): 
            x_hat = list(x_hat2)
            print('switched')
        
        if (sum(sizes[k]*x_hat[k] for k in range(n)) > capacity):
            print('oops')
            time.sleep(100)
        
        #if (i % 10 == 0):
            #print(instance_type, n, gamma, P0, size)
            
        del x_hat[-1]
        pi_hat = expected_revenue_of_assortment(n, x_hat, pref_weight, revenue, gammas, v0)  
        
        # TIME END
        end = time.time()
        
        
        # For each instance, store pi, z, and Time elapsed for solving max-cut problem
        soln_list.append([pi_hat, z_hat, min(pi_hat / z_hat * 100, 100), end - start])
    ###########################################################################
        
    # Create and write to file with name f
    with open(f, 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(soln_list)
    
    # return this solution so that we can compute the averages
    return soln_list
      
      
################# Tests for functions go beyond this point #####################

def printf(i):
    print(i)

min_ratio = 100
ratios = [101]*100


################### Generate the 36 different parameter combos ################

instance_type = [0,1]
num_products = [50]
gammas = [0.1, 0.5, 1.0]
P0s = [0.25, 0.75]
sizes = [0.1, 0.25, 0.5, 1]
capacity = 1


#final_table = ['T', 'n', '\gamma', 'P0', 'Avg', '5th', '95th', 'Std Dev.', 'CPU Secs']
final_table = []
for inst_type in instance_type:
    for n in num_products:
        for gamma in gammas:
            for P0 in P0s:
                for size in sizes:
                    print(inst_type)
                    soln = generate_and_solve_instance(gamma, P0, inst_type, n, capacity, size)
                    entry = [];
                    if inst_type == 0:
                        entry.append('I')
                    else:
                        entry.append('C')
                    entry = entry + [n, gamma, P0]
                    ratios = np.sort(np.array(soln)[:,2])
                    entry.append(np.average(ratios))
                    entry.append(ratios[int(0.04 * len(ratios))])
                    entry.append(ratios[int(0.94 * len(ratios))])
                    entry.append(np.std(ratios, axis = 0))
                    entry.append(np.average(np.array(soln)[:,3]))
                    
                    final_table.append(entry)

            
            
            
            
            
with open('final_knapsack.csv', 'wb') as my_file:
        writer = csv.writer(my_file)
        writer.writerows(final_table)           
            
            
            
for j in range(12):
    i = 4*j
    curr1 = final_table[i]
    curr2 = final_table[i+1]
    curr3 = final_table[i+2]
    curr4 = final_table[i+3]
    print('$(' + curr1[0] + ', ' + str(curr1[1]) + ', ' + str(curr1[2]) + ', ' + str(curr1[3]) + ', 0.10' + ')$& ' + str(round(curr1[4],2)) + '&' + str(round(curr1[5],2)) + '&' + str(round(curr1[6],2)) + '&' + str(round(curr1[7],2)) + '&' + str(round(curr1[8],2)) + '\\\\') 
    print('$(' + curr2[0] + ', ' + str(curr2[1]) + ', ' + str(curr2[2]) + ', ' + str(curr2[3]) + ', 0.25' + ')$& ' + str(round(curr2[4],2)) + '&' + str(round(curr2[5],2)) + '&' + str(round(curr2[6],2)) + '&' + str(round(curr2[7],2)) + '&' + str(round(curr2[8],2)) + '\\\\') 
    print('$(' + curr3[0] + ', ' + str(curr3[1]) + ', ' + str(curr3[2]) + ', ' + str(curr3[3]) + ', 0.50' + ')$& ' + str(round(curr3[4],2)) + '&' + str(round(curr3[5],2)) + '&' + str(round(curr3[6],2)) + '&' + str(round(curr3[7],2)) + '&' + str(round(curr3[8],2)) + '\\\\') 
    print('$(' + curr4[0] + ', ' + str(curr4[1]) + ', ' + str(curr4[2]) + ', ' + str(curr4[3]) + ', 1.0' + ')$& ' + str(round(curr4[4],2)) + '&' + str(round(curr4[5],2)) + '&' + str(round(curr4[6],2)) + '&' + str(round(curr4[7],2)) + '&' + str(round(curr4[8],2)) + '\\\\') 
    print('\\hline')
    
   
           
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            