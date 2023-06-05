from pulp import LpProblem, LpMinimize, LpVariable, LpInteger
from gurobipy import *
from pulp import LpProblem, LpMinimize, LpVariable, lpSum



class OptimizationModel:
    def __init__(self):
        self.model = None

   
    def build_model(self, *args, **kwargs):
        pass



# class PulpModel(OptimizationModel):
#     def __init__(self):
#         super().__init__()

#     def build_model(self, D, S, c):
#         self.model = LpProblem("SupplyChain", LpMinimize)

#         # 定义决策变量
#         self.x = LpVariable.dicts("x", ((i, j) for i in D.keys() for j in S.keys()), lowBound=0, cat='Integer')

#         # 设置目标函数
#         self.model += lpSum(c[i][j] * self.x[i, j] for i in D.keys() for j in S.keys() if (i, j) in self.x.keys())

#         # 添加约束条件
#         for i in D.keys():
#             self.model += lpSum(self.x[i, j] for j in S.keys() if (i, j) in self.x.keys()) == sum(D[i].values())
#         for j in S.keys():
#             self.model += lpSum(self.x[i, j] for i in D.keys() if (i, j) in self.x.keys()) <= sum(S[j].values())



class PulpModel(OptimizationModel):
    def __init__(self):
        super().__init__()

    def build_model(self, D, S, c):
        self.model = LpProblem("SupplyChain", LpMinimize)

        # 定义决策变量
        self.x = LpVariable.dicts("x", (D.keys(), S.keys()), lowBound=0, cat='Integer')

        # 设置目标函数
        self.model += lpSum(c[i] * self.x[i][j] for i in D.keys() for j in S.keys())

        # 添加约束条件
        for i in D.keys():
            self.model += lpSum(self.x[i][j] for j in S.keys()) == D[i]
        for j in S.keys():
            self.model += lpSum(self.x[i][j] for i in D.keys()) <= S[j]




class GurobiModel(OptimizationModel):
    def __init__(self):
        self.model = Model("SupplyChain")
        self.x = None

    def build_model(self, D, S, c):
        # 定义决策变量
        self.x = self.model.addVars(D.keys(), S.keys(), vtype=GRB.INTEGER, name="x")
        print(f"D: {D}")
        print(f"S: {S}")
        print(f"c: {c}")
        # 设置目标函数: 最小化总运输成本
        self.model.setObjective(quicksum(c[i] * self.x[i, j] for i in D.keys() for j in S.keys()), GRB.MINIMIZE)

        # 添加约束条件: 每个用户的需求必须得到满足
        for i in D.keys():
            self.model.addConstr(quicksum(self.x[i, j] for j in S.keys()) == D[i])

        # 添加约束条件: 不能超过仓库的库存量
        for j in S.keys():
            self.model.addConstr(quicksum(self.x[i, j] for i in D.keys()) <= S[j])



import pygad
import numpy

class GeneticAlgorithmModel(OptimizationModel):
    def __init__(self):
        super().__init__()
        self.ga_instance = None
        self.function_inputs = None
        self.desired_output = None
        self.solution = None
        self.solution_fitness = None
        self.solution_idx = None
        self.last_fitness = 0

    def fitness_func(self, ga_instance, solution, solution_idx):
        function_inputs = numpy.array(list(self.function_inputs))  # Convert to numpy array
        output = numpy.sum(solution * function_inputs)
        fitness = 1.0 / numpy.abs(output - self.desired_output)
        return fitness


    def callback_generation(self, ga_instance):
        print("Generation = {generation}".format(generation=ga_instance.generations_completed))
        print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
        print("Change     = {change}".format(change=ga_instance.best_solution()[1] - self.last_fitness))
        self.last_fitness = ga_instance.best_solution()[1]

    def build_model(self, function_inputs, desired_output, num_generations=100, num_parents_mating=7, sol_per_pop=50):
        self.function_inputs = function_inputs
        self.desired_output = desired_output

        num_genes = len(function_inputs)

        self.ga_instance = pygad.GA(num_generations=num_generations,
                                    num_parents_mating=num_parents_mating, 
                                    fitness_func=self.fitness_func,
                                    sol_per_pop=sol_per_pop, 
                                    num_genes=num_genes,
                                    on_generation=self.callback_generation)
    def run(self):
        self.ga_instance.run()

        # After the generations complete, some plots are showed that summarize the how the outputs/fitness values evolve over generations.
        self.ga_instance.plot_fitness()

        # Returning the details of the best solution.
        self.solution, self.solution_fitness, self.solution_idx = self.ga_instance.best_solution()
        print("Parameters of the best solution : {solution}".format(solution=self.solution))
        print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=self.solution_fitness))
        print("Index of the best solution : {solution_idx}".format(solution_idx=self.solution_idx))

        prediction = numpy.sum(numpy.array(self.function_inputs)*self.solution)
        print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

        if self.ga_instance.best_solution_generation != -1:
            print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=self.ga_instance.best_solution_generation))
