"""
This file implements a (pure) branch-and-bound algorithm to solve a (pure) integer (linear) program (IP). 

Several heuristics are used. These are implemented in the file heuristics.py. 

Roughly speaking, the algorithm works as follows: 
    First, the linear programming (LP) relaxation is solved. 
    If the optimal solution is nonintegral (what is typically the case), a fractional entry is chosen. 
    Based on this entry two further subproblems are created which are examined afterwards. 
    Therefore, during the algorithm a binary tree is built where each node corresponds to a subproblem.
    Moreover, during the algorithm lower and upper bounds on the optimal value are maintained. 
    Based on these bounds, it is possible to prune certain subproblems in order to speed up the algorithm.
"""

from gurobipy import GRB
import numpy as np
from math import *
from aux_fct import terminate, termination_reason, solve_root_lp, is_int


def branch_and_bound(A,b,c, parameters):
    """This method solves an optimization problem of the form
                    maximize    c*x
                    subject to  Ax <= b
                                x >= 0 
                                x integer 
        using a so called branch-and-bound algorithm. 

        The algorithm requires a dictionary containing the following parameters:
            pick_subproblem             Heuristic/function to select the next subproblem
            pick_variable               Heuristic/function to select the next variable to branch at
            feasibility_heuristic       Heuristic/function trying to find a feasible point for the IP
            max_iter                    Maximum number of iterations to perform
            opt_gap                     Relative gap between lower and upper bound to terminate the algorithm

        The output consists of a dictionary containing infomation about the found solution, i.e. 
            x                           (Approximately) optimal solution
            OPT                         Objective value of the (approximately) optimal solution
        as well as a dictionary containing some statistics about the solving process, i.e.
            exitflag                    Reason for termination
            iterations                  Number of iterations (= examined subproblems)
            gap                         Relative gap between lower and upper bound 
            lower bounds                Lower bounds found during the algorithm (induced by feasible points) 
            upper bounds                Upper bounds found during the algorithm (induced by LP relaxations)
       """
    
    # Solve root LP
    root = solve_root_lp(A,b,c)

    # Distinguish several cases based on LP solution
    if root.status == GRB.INFEASIBLE:
        return None, {"exitflag": "Infeasible", "iterations": 0, "gap": None, "lower bounds": None, "upper bounds": None}
    if root.status == GRB.UNBOUNDED:
        solution, statistics = branch_and_bound(A,b,np.zeros_like(c),parameters)
        if statistics["exitflag"] ==  "Infeasible":
            return None, {"exitflag": "Infeasible", "iterations": 0, "gap": None, "lower bounds": None, "upper bounds": None}
        else:
            return None, {"exitflag": "Unbounded", "iterations": statistics["iterations"], "gap": None, "lower bounds": None, "upper bounds": None}
    if root.status == GRB.OPTIMAL :
        if is_int(root.getAttr('X', root.getVars())):
            return {"x": root.getAttr('X', root.getVars()), "OPT": root.ObjVal}, {"exitflag": "Optimal", "iterations": 0, "gap": 0,
                                                                                  "lower bounds": [root.ObjVal], "upper bounds":[root.ObjVal]}
    else:
        raise Exception("Unknown error occurred when solving the root LP. Please reconsider your problem formulation.") 

    # Initialize bounds
    upper_bound = root.ObjVal       # Optimal value of LP relaxation
    upper_bounds = [upper_bound]
    best_solution = None            # Feasible solution with best objective value 
    lower_bound = -np.inf           # Objective value of best feasible solution
    lower_bounds = [lower_bound]
    
    # Try to find a feasible point heuristically
    heuristic_solution = parameters["feasibility_heuristic"](A,b,root.getAttr('X', root.getVars()))
    if heuristic_solution != None:
        best_solution   = heuristic_solution            
        lower_bound     = c@heuristic_solution           
        lower_bounds[0] = lower_bound

    # Initialize search tree. Each subproblem is described by its Gurobi model, its optimal value and its optimal solution.
    subproblems = []
    subproblems.append({"Model": root, "OPT": root.ObjVal, "x*": root.getAttr('X', root.getVars())})

    iter = 0
    while not terminate(parameters["opt_gap"], lower_bound, upper_bound, parameters["max_iter"], iter, subproblems):
        # Pick a subproblem
        parent, x = parameters["pick_subproblem"](subproblems)
        # Pick a fractional variable
        branching_index = parameters["pick_variable"](x)           

        # Branch w.r.t the fractional variable and create two subproblems 
        child_left = parent.copy()
        child_left.addConstr(child_left.getVars()[branching_index] <= floor(x[branching_index]))
        child_left.optimize()       
        if child_left.status == GRB.OPTIMAL and child_left.ObjVal > lower_bound:
            if is_int(child_left.getAttr('X', child_left.getVars())):
                lower_bound = child_left.ObjVal
                best_solution = child_left.getAttr('X', child_left.getVars())    
            else:
                subproblems.append({"Model": child_left, "OPT": child_left.ObjVal, "x*": child_left.getAttr('X', child_left.getVars())})

        child_right = parent.copy()
        child_right.addConstr(child_right.getVars()[branching_index] >= ceil(x[branching_index]))
        child_right.optimize()
        if child_right.status == GRB.OPTIMAL and child_right.ObjVal > lower_bound:
            if is_int(child_right.getAttr('X', child_right.getVars())):
                lower_bound = child_right.ObjVal
                best_solution = child_right.getAttr('X', child_right.getVars())    
            else:
                subproblems.append({"Model": child_right, "OPT": child_right.ObjVal, "x*": child_right.getAttr('X', child_right.getVars())})

        # Update bounds
        if subproblems != []:
            upper_bound = max(max(subproblem["OPT"] for subproblem in subproblems), lower_bound)
        else:
            upper_bound = lower_bound
        upper_bounds.append(upper_bound)
        lower_bounds.append(lower_bound)

        iter += 2


    # Return solution
    if lower_bound != -np.inf:
        gap = (upper_bound - lower_bound) / lower_bound if lower_bound != 0 else None
        solution = {"x": best_solution, "OPT": lower_bound}
        statistics = {"exitflag": termination_reason(parameters["opt_gap"], lower_bound, upper_bound, parameters["max_iter"], iter), 
                      "iterations": iter, "gap": gap, "lower bounds": lower_bounds, "upper bounds": upper_bounds}
    else:
        solution = None
        statistics = {"exitflag": "Infeasible","iterations": iter, "gap": None, "lower bounds": None, "upper bounds": None}

    return solution, statistics


