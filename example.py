"""
This file illustrates the use of the branch-and-bound solver from main.py using a concrete example.

Moreover, the development of the lower and upper bounds along the algorithm is plotted.
"""

import numpy as np 
from main import branch_and_bound
from heuristics import pick_subproblem, pick_variable, feasibility_heuristic
from plot_optimality_gap import plot_optimality_gap


# Create a randomized test instance
n = 30  
m = 60  
A = np.random.randint(1,10,m*n).reshape(m,n)
b = np.random.randint(n,50*n,m)
c = np.random.randint(-10,10,n)

# Solve the integer linear program
parameters = {"pick_subproblem": pick_subproblem, "pick_variable": pick_variable, "feasibility_heuristic": feasibility_heuristic, 
              "max_iter": 10000, "opt_gap": 0.0001}
solution, statistics = branch_and_bound(A,b,c, parameters)

# Access the optimal solution
print("Optimal value: ", solution["OPT"])
print("Optimal solution: ", solution["x"])

# Access statistics about the solving process
print("Termination status: ", statistics["exitflag"])
print("Number of iterations: ", statistics["iterations"])
print("Relative optimality gap: ", statistics["gap"])
print("Lower bounds: ", statistics["lower bounds"])
print("Upper bounds: ", statistics["upper bounds"])

# Plot development of the optimality gap and store the image
plot_optimality_gap(A,b,c, parameters)




