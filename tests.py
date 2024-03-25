"""
This file implements several tests for the branch & bound algorithm in main.py.

Firstly, all cases of LP-IP behaviour are tested via two-dimensional examples.
Secondly, the algorithm is tested against the commercial solver Gurobi.
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
from math import *
from main import branch_and_bound
from heuristics import pick_subproblem, pick_variable, feasibility_heuristic


parameters = {"pick_subproblem": pick_subproblem, "pick_variable": pick_variable, "feasibility_heuristic": feasibility_heuristic, 
              "max_iter": 10000, "opt_gap": 0.0001}


# Infeasible LP
A = np.array([[1,0],
             [-1,0]])
b = np.array([1,-2])
c = np.array([1,1])
branch_and_bound(A,b,c,parameters)

# Integral LP solution
A = np.array([[1,0],
             [0,1]])
b = np.array([2,3])
c = np.array([1,1])
branch_and_bound(A,b,c,parameters)

# Unbounded LP and IP
A = np.array([[1,0],
             [0,0]])
b = np.array([2,0])
c = np.array([1,1])
branch_and_bound(A,b,c,parameters)

# Unbounded LP and infeasible IP
A = np.array([[0,-1],
             [0,1]])
b = np.array([-1/4,3/4])
c = np.array([1,1])
branch_and_bound(A,b,c,parameters)

# Solvable LP and infeasible IP
A = np.array([[-1,0],
             [1,0],
             [0,-1],
             [0,1]])
b = np.array([-1/4,3/4,-1/4,3/4])
c = np.array([1,1])
branch_and_bound(A,b,c,parameters)

# Solvable LP and solvable IP
A = np.array([[1,0],
             [0,1]])
b = np.array([2.3,3.5])
c = np.array([1,1])
branch_and_bound(A,b,c,parameters)




# Test against Gurobi

# Create a randomized test instance
n = 50  
m = 100  
A = np.random.randint(1,10,m*n).reshape(m,n)
b = np.random.randint(n,50*n,m)
c = np.random.randint(-10,10,n)

# Solve IP with algorithm from main.py
solution, statistics = branch_and_bound(A,b,c, parameters)

# Solve IP using Gurobi
model = gp.Model('IP')
model.params.DualReductions = 0     
model.params.LogToConsole = 0       
x = model.addMVar(shape=np.shape(c),name='x', vtype=GRB.INTEGER)          
model.addConstr(A@x <= b)
model.setObjective(c@x, GRB.MAXIMIZE)
model.optimize()

# Compare the optimal values
print("Relative gap main.py vs Gurobi: ", (model.ObjVal - solution["OPT"]) / solution["OPT"])
