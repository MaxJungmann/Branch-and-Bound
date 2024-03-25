"""
This file plots the development of the absolute and relative gap between lower and upper bounds along the 
branch-and-bound algorithm from main.py.
"""

import numpy as np 
import matplotlib.pyplot as plt 
from main import branch_and_bound
from heuristics import pick_subproblem, pick_variable, feasibility_heuristic


parameters = {"pick_subproblem": pick_subproblem, "pick_variable": pick_variable, "feasibility_heuristic": feasibility_heuristic, 
              "max_iter": 10000, "opt_gap": 0.001}


def plot_optimality_gap(A,b,c, parameters):
    """ Requires problem description given by A,b,c and parameters for the branch & bound algorithm in main.py. 

        Plots absolute and relative optimality gap in each iteration.
    """

    # Solve IP
    solution ,statistics = branch_and_bound(A,b,c,parameters)

    # Set lower bounds of -inf to None
    statistics["lower bounds"] = [lb if lb != -np.inf else None for lb in statistics["lower bounds"]]
    
    # Set up the plot 
    fig,ax = plt.subplots(1,2)
    fig.set_size_inches(12,8)
    plt.subplots_adjust(wspace=0.25)
    plt.rcParams['text.usetex'] = True

    # Plot absolute optimality gap
    ax[0].plot(statistics["upper bounds"], label="Upper bounds", c='r', linewidth=3)
    ax[0].plot(statistics["lower bounds"], label="Lower bounds",c='b', linewidth=3)
    ax[0].set_xlabel("Number of iterations")
    ax[0].set_ylabel("Objective value")
    ax[0].set_title("Absolute optimality gap")
    ax[0].legend()

    # Plot relative optimality gap
    relative_gap = []
    for i in range(len(statistics["lower bounds"])):
        if statistics["lower bounds"][i] == None:
            relative_gap.append(None)
        else:
            relative_gap.append((statistics["upper bounds"][i] - statistics["lower bounds"][i]) / statistics["lower bounds"][i])
    ax[1].plot(relative_gap, linewidth=3, c='k')
    ax[1].set_xlabel("Number of iterations")
    ax[1].set_ylabel(r"$\frac{upper \ bound - lower \ bound}{lower \ bound}$")
    ax[1].set_title("Relative optimality gap")

    plt.savefig("optimality_gap.png")
    plt.show()

