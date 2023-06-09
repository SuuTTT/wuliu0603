## 线性建模

### pulp blockchain

```python
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
```

验证

The provided code defines a transportation optimization problem. Based on your description, it seems like your problem is a version of the classic transportation problem. The transportation problem is a type of network flow problem where the goal is to find the cheapest way to ship goods from several origins (e.g., warehouses) to several destinations (e.g., customers), subject to supply constraints at the origins and demand constraints at the destinations.

Your problem can indeed be solved using the Pulp linear programming library, as it seems you have structured the problem correctly, assuming the 'c' variable represents the transportation costs. The assumptions here are:

1. The costs, demand and supply quantities are given as dictionary items indexed by the respective warehouse and customer indices.
2. The function `test_data_reader()` reads the data properly and returns a dictionary where 'DemandProduct', 'WarehouseProduct', and 'TransportationProduct' are keys, and the values are pandas dataframes where 'Quantity' or 'Stock' are columns.
3. The PulpModel and PulpSolver classes are defined correctly (since they aren't given in your example).

Also, if the warehouses have a limited delivery range, you would need to add constraints to your model to reflect this. In your given code, this limitation is not included.

Finally, please note that the PuLP library in Python allows you to solve optimization problems, but cannot guarantee the 'best' solution in all cases as this heavily depends on the specific problem, the quality of the provided data, and the correct formulation of the problem. If there are special conditions that have not been reflected in your model, the resulting solution may not be applicable to the real-world situation.

## gene

### code explain

在这个问题中，我们使用遗传算法（Genetic Algorithm，GA）进行建模和解决。遗传算法是一种启发式搜索和优化方法，它借鉴了自然界中的进化论和自然选择机制。

### 1. 定义适应度函数

适应度函数是遗传算法的核心，它定义了如何衡量一个解（即一个个体或者一组基因）的质量。在这个问题中，我们定义的适应度函数是这样的：

```python
def fitness_func(self, ga_instance, solution, solution_idx):
    function_inputs = numpy.array(list(self.function_inputs))  # Convert to numpy array
    output = numpy.sum(solution * function_inputs)
    fitness = 1.0 / numpy.abs(output - self.desired_output)
    return fitness
```

在这个函数中，我们首先将解乘以问题的输入，然后计算其和，这个和表示的是该解的预测输出。我们希望这个预测输出能够尽可能接近我们期望的输出，因此我们将预测输出与期望输出之间的绝对差值作为适应度函数。我们希望最小化这个差值，所以我们取其倒数作为适应度。

### 2. 构建遗传算法模型

在构建遗传算法模型时，我们需要设置一些参数，包括种群大小、基因数量、父母数量以及进化代数等。

```python
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
```

### 3. 运行模型

最后，我们可以运行模型并打印出每一代的最佳解和最佳适应度。运行结束后，我们可以获取最佳解以及对应的预测输出和适应度。

```python
def run(self):
    self.ga_instance.run()
    self.ga_instance.plot_fitness()
    self.solution, self.solution_fitness, self.solution_idx = self.ga_instance.best_solution()
```

这就是我们如何使用遗传算法进行建模和解决这个问题的方法。

## prompt

```
Traceback (most recent call last):
  File "/mnt/e/suu/workplace/wuliu/test_algo.py", line 58, in <module>
    test_model_builder_and_solver(model_type)
  File "/mnt/e/suu/workplace/wuliu/test_algo.py", line 50, in test_model_builder_and_solver
    model_builder.build_model(D, S, c)
TypeError: GeneticAlgorithmModel.build_model() takes 2 positional arguments but 4 were given
---
pygad example usage
import pygad
import numpy

"""
Given the following function:
    y = f(w1:w6) = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + 6wx6
    where (x1,x2,x3,x4,x5,x6)=(4,-2,3.5,5,-11,-4.7) and y=44
What are the best values for the 6 weights (w1 to w6)? We are going to use the genetic algorithm to optimize this function.
"""

function_inputs = [4,-2,3.5,5,-11,-4.7] # Function inputs.
desired_output = 44 # Function output.

def fitness_func(ga_instance, solution, solution_idx):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    output = numpy.sum(solution*function_inputs)
    fitness = 1.0 / numpy.abs(output - desired_output)
    return fitness

fitness_function = fitness_func

num_generations = 100 # Number of generations.
num_parents_mating = 7 # Number of solutions to be selected as parents in the mating pool.

# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 50 # Number of solutions in the population.
num_genes = len(function_inputs)

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop, 
                       num_genes=num_genes,
                       on_generation=callback_generation)

# Running the GA to optimize the parameters of the function.
ga_instance.run()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

prediction = numpy.sum(numpy.array(function_inputs)*solution)
print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

if ga_instance.best_solution_generation != -1:
    print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

# Saving the GA instance.
filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
ga_instance.save(filename=filename)

# Loading the saved GA instance.
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_fitness()
---
please give me the correct class GeneticAlgorithmModel, you can rewrite it totally
```
