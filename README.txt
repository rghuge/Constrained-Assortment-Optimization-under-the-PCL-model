DESCRIPTION

This repository contains the code associated with the paper "Constrained Assortment Optimization under the PCL model". The code is split into three parts:
(1) Unconstrained/Capacitated assortment optimization
(2) Knapsack constrained assortment optimization
(3) Partition constrained assortment optimization

DATA

We also provide the data used to generate the results in the unconstrained/capacitated cases. The structure of the data is as follows: 
(i) The data files are labeled according to their parameter configuration. For example, the file "data_cons_1_50_0.5_0.25_0.8.txt" contains capacitated data associated with the independent instances with 50 product types having gamma = 0.5, P0 = 0.25 and delta = 0.8.
(ii) Each data file contains 100 instances corresponding to a specific parameter setting.
(iii) The first line of each instance contains the preference weight values - i.e. there are n 'comma' separated values that correspond to the preference weights of the products.
(iv) The second line, in an analogous way, contains the revenues of the products.
(v) Then n lines follow. Each of these lines contains a row of the dissimilarity matrix.

RUNNING THE CODE
The files "main-uncap", "main-cap", "main-knapsack", and "main-partition" should be run to start executing the algorithms for the corresponding constrained assortment problem.

OUTPUT
Two kinds of outputs are saved to file:
(1) For each parameter setting, we save some information about the 100 test instances. We save the final revenue obtained, an upper bound on the optimal revenue, the ratio of revenue obtained to the upper bound on the optimal revenue, and the time taken for execution.
(2) For each constrained assortment problem, we save the aggregate result for each parameter setting in a single file. We record a few statistics of the results - average ratio achieved, the minimum ratio over the 100 instances, the 5th, and 95th percentile, and the standard deviation among the ratios, and the time taken on average for execution. 