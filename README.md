# Branch-and-Bound algorithm for solving integer programs

To deepen my understanding about Integer Programming I implemented a branch-and-bound algorithm in Python. A branch-and-bound algorithm is the standard approach to solve general integer (linear) programs (IPs). 
An integer program is a discrete optimization problem of the form

$$\begin{equation} \tag{IP}
    \begin{aligned} 
        \text{maximize} \quad    & c^\top x \\
        \text{subject to} \quad  & Ax <= b \\
                                 & x \geq 0 \\
                                 & x \in \mathbb{Z}^n .
    \end{aligned}
\end{equation}$$

For a thorough introduction to Integer Programming see for instance [here](https://web.mit.edu/15.053/www/AMP-Chapter-09.pdf). Section 9.5 also explains the branch-and-bound algorithm in detail. 

The basic idea of this branch-and-bound algorithm is to iteratively solve refined linear programming (LP) relaxations of the integer program (i.e. to allow also fractional values for the variables). In order to solve these LP relaxations along the algorithm I used the commercial solver Gurobi. A free academic Gurobi license can be obtained from [here](https://www.gurobi.com/academia/academic-program-and-licenses/).

Moreover, the algorithm maintains and improves upper and lower bounds for the optimal value in each iteration. As soon as these bounds are close enough to each other the algorithm terminates. The image below shows the absolute and relative behaviour of these bounds for a specific instance. 

![](/optimality_gap.png)


# Project organization
1. The actual algorithm is implemented in [main.py](/main.py) and uses some auxiliary functions from [aux_fct.py](/aux_fct.py). Moreover, the algorithm requires several user-defined heuristics to make certain decisions along the algorithm. These are implemented in [heuristics.py](/heuristics.py). Feel free to modify these heuristics for your own purposes!
2. The file [example.py](/example.py) illustrates the usage of the algorithm on a randomized sample problem. The development of the optimality gap is plotted using [plot_optimality_gap.py](/plot_optimality_gap.py) and is saved to [optimality_gap.png](/optimality_gap.png).
3. The implementation is tested in [tests.py](/tests.py).


