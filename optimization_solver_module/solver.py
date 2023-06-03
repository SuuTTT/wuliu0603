
from pulp import LpSolverDefault, PULP_CBC_CMD
from gurobipy import *
# 在 optimization_solver_module 下
class OptimizationSolver:
    def __init__(self, model):
        self.model = model

    
    def solve_model(self, *args, **kwargs):
        pass



class PulpSolver(OptimizationSolver):
    def __init__(self, model_builder):
        super().__init__(model_builder.model)
        self.model_builder = model_builder

    def solve_model(self):
        self.model_builder.model.solve(PULP_CBC_CMD())
        if self.model_builder.model.status == 1:  # 1 stands for "Optimal" in PuLP
            return {v.name: v.varValue for v in self.model_builder.model.variables()}
        else:
            print("No solution found")
            return None


    


class GurobiSolver(OptimizationSolver):
    def __init__(self, model):
        self.model = model

    def solve_model(self):
        self.model.optimize()
        if self.model.status == GRB.OPTIMAL:
            solution = self.model.getAttr('x', self.model.getVars())
            return {var.VarName: var.x for var in self.model.getVars()}
        else:
            print("No solution found")
            return None


import pygad

class GASolver(OptimizationSolver):
    def __init__(self, ga_instance):
        self.ga_instance = ga_instance

    def solve_model(self):
        # Run the GA to optimize the parameters of the function.
        self.ga_instance.run()

        # Get the details of the best solution.
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()

        if solution_fitness is None:
            print("No solution found")
            return None
        else:
            return {"solution": solution, "fitness": solution_fitness, "index": solution_idx}

