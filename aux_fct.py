""" This file implements several auxiliary functions for the branch-and-bound algorithm in main.py. """

import gurobipy as gp
from gurobipy import GRB
import numpy as np


def terminate(opt_gap, lower_bound, upper_bound, max_iter, iter,subproblems):
    if lower_bound != 0:
        if np.abs((upper_bound - lower_bound) / lower_bound) <= opt_gap:        
            return True
    if np.abs(upper_bound - lower_bound) <= 0.01:        
        return True
    if iter > max_iter:      
        return True
    if subproblems == []:
        return True


def termination_reason(opt_gap, lower_bound, upper_bound, max_iter, iter):
    if lower_bound != 0:
        if np.abs((upper_bound - lower_bound) / lower_bound) <= opt_gap:
            return "Optimal"
    if np.abs(upper_bound - lower_bound) <= 0.01:        
        return "Optimal"
    if iter > max_iter:
        return "Maximum number of iterations reached"


def solve_root_lp(A,b,c):
    root = gp.Model('Root LP')
    root.params.DualReductions = 0     # Distinguish between infeasible and unbounded problems
    root.params.LogToConsole = 0       # Make Gurobi quiet

    x = root.addMVar(shape=np.shape(c),name='x')          # x >= 0 by default
    root.addConstr(A@x <= b)
    root.setObjective(c@x, GRB.MAXIMIZE)
    root.optimize()

    return root


def is_int(x):
    return all(i.is_integer() for i in x)
