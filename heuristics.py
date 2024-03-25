"""
This file implements several heuristics for the branch-and-bound algorithm in main.py.

It consists of the following methods:
    1. A heuristic to select the node/subproblem which will be examined next.
    2. A heuristic to select the (fractional) variable to branch at.
    3. A heuristic to find a feasible point for the IP.
"""

import numpy as np
from math import *


def pick_subproblem(subproblems, method="Best-First"):
    if method == "Best-First":
        index = np.argmax([subproblem["OPT"] for subproblem in subproblems])    
    if method == "DFS":
        index = -1
    if method == "BFS":
        index = 0

    model, x = [subproblems[index].get(key) for key in ["Model", "x*"]]
    del subproblems[index]
    return model, x


def pick_variable(x):
    # Return index of first nonintegral variable
    for (index, value) in enumerate(x):
        if not value.is_integer():
            return index


def feasibility_heuristic(A,b,x):
    # Rounding down
    x_down = [floor(xi) for xi in x]
    if all(A@x_down <= b):
        return x_down
    
    # Rounding up
    x_up = [ceil(xi) for xi in x]
    if all(A@x_up <= b):
        return x_up
    
    # Randomized rounding based on fractional part
    x_random = [floor(xi) + np.random.binomial(1, xi - floor(xi)) for xi in x]
    if all(A@x_random <= b):
        return x_random
    
    # All zero vector
    x_zero = [0 for xi in x] 
    if all(A@x_zero <= b):
        return x_zero
    
    else:
        return None


