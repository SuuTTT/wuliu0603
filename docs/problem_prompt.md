# 在大项目中使用chatGPT的最佳实践

## Rich Prompt

尽可能罗列最相关的信息，最后给出命令。

### DebugPrompt

格式:

```
背景intro
---
代码片段 1~n
---
报错信息 1~n
---

newbing or GPT4browser搜索整理的解决方案
---
命令
```

例子

```
this section is background, not my final prompt, don't ask it.
Title: Optimal Logistics Planning under Configurable Cost Function

Problem Description:

You are tasked to design a system for managing a logistics distribution network. The network consists of multiple warehouses, each of which has a fixed location and a certain amount of inventory for various items. There are also multiple users, each with a fixed location and specific item demands.

The objective is to devise an optimal logistics plan to satisfy all user demands while minimizing the total transportation cost. This problem assumes that each warehouse has a limited distribution range.

The cost function for transporting items can be configured. This means that it can be a linear function, a piecewise function, or any other forms of function, determined by certain parameters. 

The input includes:

1. User demand list: Specifies what items each user needs and the amount of each item.
2. Warehouse inventory: Specifies the quantity of each item in every warehouse.
3. Configurable cost function: The cost function can take different forms (linear, piecewise, etc.) to compute the cost of transporting a quantity x of item k from warehouse i to user j.

The output should include:

1. A logistics plan: This consists of several lines, each in the form of "warehouse ID - item ID - user ID - item quantity".
2. User satisfaction information: The items received by each user and their corresponding satisfaction levels.

Constraints:

- All users' demands must be satisfied.
- The transportation volume for each item should not exceed the warehouse's inventory.
- The transportation volume for each item must be an integer.
- The system should be able to handle the configurable cost function.

The goal is to find the logistics plan with the minimum cost that can satisfy all user demands.
---
this section is the database

CREATE TABLE Grid (
  GridID INT PRIMARY KEY,
  LeftLongitude DOUBLE,
  RightLongitude DOUBLE,
  UpperLatitude DOUBLE,
  LowerLatitude DOUBLE
);
CREATE TABLE User (
  UserID INT PRIMARY KEY,
  Longitude DOUBLE,
  Latitude DOUBLE,
  Priority INT
);
CREATE TABLE Product (
  ProductID INT PRIMARY KEY,
  Category VARCHAR(255),
  Name VARCHAR(255),
  Abbreviation VARCHAR(255),
  Unit VARCHAR(255)
);

CREATE TABLE Warehouse (
  WarehouseID INT PRIMARY KEY,
  Longitude DOUBLE,
  Latitude DOUBLE,
  CoverageRange DOUBLE
);
CREATE TABLE WarehouseProduct (
  WarehouseID INT,
  ProductID INT,
  Stock INT,
  MinStock INT,
  MaxStock INT,
  PRIMARY KEY (WarehouseID, ProductID),
  FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
CREATE TABLE Transportation (
  TransportID INT PRIMARY KEY,
  StartWarehouseID INT,
  EndLongitude DOUBLE,
  EndLatitude DOUBLE,
  CostTime INT,
  FOREIGN KEY (StartWarehouseID) REFERENCES Warehouse(WarehouseID)
);
CREATE TABLE TransportationProduct (
  TransportID INT,
  ProductID INT,
  Quantity INT,
  PRIMARY KEY (TransportID, ProductID),
  FOREIGN KEY (TransportID) REFERENCES Transportation(TransportID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
CREATE TABLE Demand (
  DemandID INT PRIMARY KEY,
  StartEarliestTime DATETIME,
  StartLatestTime DATETIME,
  EndEarliestTime DATETIME,
  EndLatestTime DATETIME,
  UserID INT,
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);
CREATE TABLE DemandProduct (
  DemandID INT,
  ProductID INT,
  Quantity INT,
  PRIMARY KEY (DemandID, ProductID),
  FOREIGN KEY (DemandID) REFERENCES Demand(DemandID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
---
this section is the test code

CREATE TABLE Grid (
  GridID INT PRIMARY KEY,
  LeftLongitude DOUBLE,
  RightLongitude DOUBLE,
  UpperLatitude DOUBLE,
  LowerLatitude DOUBLE
);
CREATE TABLE User (
  UserID INT PRIMARY KEY,
  Longitude DOUBLE,
  Latitude DOUBLE,
  Priority INT
);
CREATE TABLE Product (
  ProductID INT PRIMARY KEY,
  Category VARCHAR(255),
  Name VARCHAR(255),
  Abbreviation VARCHAR(255),
  Unit VARCHAR(255)
);

CREATE TABLE Warehouse (
  WarehouseID INT PRIMARY KEY,
  Longitude DOUBLE,
  Latitude DOUBLE,
  CoverageRange DOUBLE
);
CREATE TABLE WarehouseProduct (
  WarehouseID INT,
  ProductID INT,
  Stock INT,
  MinStock INT,
  MaxStock INT,
  PRIMARY KEY (WarehouseID, ProductID),
  FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
CREATE TABLE Transportation (
  TransportID INT PRIMARY KEY,
  StartWarehouseID INT,
  EndLongitude DOUBLE,
  EndLatitude DOUBLE,
  CostTime INT,
  FOREIGN KEY (StartWarehouseID) REFERENCES Warehouse(WarehouseID)
);
CREATE TABLE TransportationProduct (
  TransportID INT,
  ProductID INT,
  Quantity INT,
  PRIMARY KEY (TransportID, ProductID),
  FOREIGN KEY (TransportID) REFERENCES Transportation(TransportID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
CREATE TABLE Demand (
  DemandID INT PRIMARY KEY,
  StartEarliestTime DATETIME,
  StartLatestTime DATETIME,
  EndEarliestTime DATETIME,
  EndLatestTime DATETIME,
  UserID INT,
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);
CREATE TABLE DemandProduct (
  DemandID INT,
  ProductID INT,
  Quantity INT,
  PRIMARY KEY (DemandID, ProductID),
  FOREIGN KEY (DemandID) REFERENCES Demand(DemandID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
---
algorithm and output:

def build_and_solve_model(data_dict, model_type):
    # Create a dictionary with demand and supply data from test data
    D = data_dict['DemandProduct']['Quantity'].to_dict()
    S = data_dict['WarehouseProduct']['Stock'].to_dict()

    # Create cost dictionary from test data
    c = data_dict['TransportationProduct']['Quantity'].to_dict()  # Assuming transportation product quantity as cost
    print(D,S,c)
    # Initialize model builder and solver based on the model type
    if model_type == 'Gurobi':
        model_builder = GurobiModel()
        solver = GurobiSolver(model_builder.model)
    elif model_type == 'Pulp':
        model_builder = PulpModel()
        solver = PulpSolver(model_builder)
solution = solver.solve_model()

    print(f"Solution for {model_type}: ", solution)

(wuliu) root@qweG611:/mnt/e/suu/workplace/wuliu0603# python main.py 
{0: 50, 1: 60, 2: 70, 3: 80} {0: 1000, 1: 1000, 2: 2000, 3: 2000} {0: 100, 1: 200, 2: 300, 3: 400}
Restricted license - for non-production use only - expires 2024-10-28
Gurobi Optimizer version 10.0.1 build v10.0.1rc0 (linux64)

CPU model: Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz, instruction set [SSE2|AVX|AVX2]
Thread count: 8 physical cores, 8 logical processors, using up to 8 threads

Optimize a model with 8 rows, 16 columns and 32 nonzeros
Model fingerprint: 0x03164fe5
Variable types: 0 continuous, 16 integer (0 binary)
Coefficient statistics:
  Matrix range     [1e+00, 1e+00]
  Objective range  [1e+02, 4e+02]
  Bounds range     [0e+00, 0e+00]
  RHS range        [5e+01, 2e+03]
Found heuristic solution: objective 70000.000000
Presolve removed 8 rows and 16 columns
Presolve time: 0.00s
Presolve: All rows and columns removed

Explored 0 nodes (0 simplex iterations) in 0.00 seconds (0.00 work units)
Thread count was 1 (of 8 available processors)

Solution count 1: 70000 

Optimal solution found (tolerance 1.00e-04)
Best objective 7.000000000000e+04, best bound 7.000000000000e+04, gap 0.0000%
Solution for Gurobi:  {'x[0,0]': 0.0, 'x[0,1]': 50.0, 'x[0,2]': -0.0, 'x[0,3]': -0.0, 'x[1,0]': -0.0, 'x[1,1]': -0.0, 'x[1,2]': 0.0, 'x[1,3]': 60.0, 'x[2,0]': 0.0, 'x[2,1]': 70.0, 'x[2,2]': -0.0, 'x[2,3]': -0.0, 'x[3,0]': -0.0, 'x[3,1]': -0.0, 'x[3,2]': 0.0, 'x[3,3]': 80.0}
(wuliu) root@qweG611:/mnt/e/suu/workplace/wuliu0603# 

---
below is the task your are going to solve:
请描述gurobi解决这个问题的过程，使用具体的数值举例
```

### generalPrompt

背景intro

---

代码框架

---

核心代码（main 函数）

---

问题

```
this
section is background, not my final prompt, don't ask it.

Title:
Optimal Logistics Planning under Configurable Cost Function

Problem
Description:

You are
tasked to design a system for managing a logistics distribution network. The
network consists of multiple warehouses, each of which has a fixed location and
a certain amount of inventory for various items. There are also multiple users,
each with a fixed location and specific item demands.

The
objective is to devise an optimal logistics plan to satisfy all user demands
while minimizing the total transportation cost. This problem assumes that each
warehouse has a limited distribution range.

The cost
function for transporting items can be configured. This means that it can be a
linear function, a piecewise function, or any other forms of function,
determined by certain parameters.

The input
includes:

1. User
   demand list: Specifies what items each user needs and the amount of each item.

2.
Warehouse inventory: Specifies the quantity of each item in every warehouse.

3.
Configurable cost function: The cost function can take different forms (linear,
piecewise, etc.) to compute the cost of transporting a quantity x of item k
from warehouse i to user j.

The output
should include:

1. A
   logistics plan: This consists of several lines, each in the form of
   "warehouse ID - item ID - user ID - item quantity".

2. User
   satisfaction information: The items received by each user and their
   corresponding satisfaction levels.

Constraints:

- All
  users' demands must be satisfied.

- The
  transportation volume for each item should not exceed the warehouse's
  inventory.

- The
  transportation volume for each item must be an integer.

- The
  system should be able to handle the configurable cost function.

The goal
is to find the logistics plan with the minimum cost that can satisfy all user
demands.

---

this section is the code framework to give
context, no need to answer

体系结构分析

基于上述需求，我们可以设计一个包含以下几个模块的算法：

1.
**数据输入模块**：负责接收和处理来自数据库的输入数据，包括用户需求列表、仓库库存、花费函数等。

2.
**物流方案生成模块**：负责根据用户需求和仓库库存，生成满足所有需求的物流方案。

3.
**优化模块**：负责在满足所有需求的前提下，优化物流方案，使得总的运输成本最小。

4.
**实时更新模块**：负责处理实时更新的用户需求和仓库库存数据，并根据新的数据更新物流方案。

5.
**数据输出模块**：负责将优化后的物流方案输出到数据库。

----

This section is the flask_app.py of code, showing how to use the
modules:  
 
# flask_app.py
from flask import Flask, request, jsonify
from data_preprocessing_module.data_preprocessor import Spdd,DPTJ
from data_read_module.data_reader import DataReader
from optimization_model_module.model_builder import GurobiModel, PulpModel, GeneticAlgorithmModel
from optimization_solver_module.solver import GurobiSolver, PulpSolver, GASolver


app = Flask(__name__)

@app.route('/getZytpcl', methods=['POST'])
def getZytpcl():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    spdd_list = [Spdd.from_dict(item) for item in data]

    results = {}
    #for model_type in ['GA','Gurobi', 'Pulp']:
    for model_type in ['Pulp']:
        result = process_order_data(spdd_list, model_type)
        converted_result = convert_result_to_dptj(model_type, result)
        results[model_type] = converted_result
    return jsonify(results)


def convert_result_to_dptj(model_type, model_result):
    dptj_list = []

    if isinstance(model_result, dict):  # Ensure model_result is of dict type
        for key, value in model_result.items():
            if key.startswith("x"):  # Process keys starting with "x"
                # Determine if the key uses commas or underscores as separators
                if "," in key:
                    key_values = key.strip("x[]").split(",")
                else:
                    key_values = key.strip("x_").split("_")

                if len(key_values) == 2:  # Make sure there are exactly 2 values
                    ckbh, yhbh = key_values  # Extract warehouse and user IDs
                    dptj = DPTJ(int(ckbh), int(yhbh), value)  # Create a DPTJ object
                    dptj_list.append(dptj.__dict__)  # Convert DPTJ object to dict for JSON serialization

    return {model_type: dptj_list}  # Return the results





from data_read_module.data_reader import DataReader

def convert_order_data(order_data):
    # Initialize empty dictionary for demand
    D = {}

    # Iterate through order_data
    for order in order_data:
        # Aggregate demand
        # Assuming 'spnm' as the product id and 'sl' as the quantity
        if order.spnm in D:
            D[order.spnm] += order.sl
        else:
            D[order.spnm] = order.sl

    # Initialize DataReader
    data_reader = DataReader("root", "qwe123", "localhost", "wuliu")

    # Read supply and cost from the database
    S = data_reader.read_data('WarehouseProduct')['Stock'].to_dict()
    c = data_reader.read_data('TransportationProduct')['Quantity'].to_dict()  # Assuming transportation product quantity as cost

    return D, S, c

def process_order_data(order_data, model_type):
    # Convert order_data into a format that your model can consume
    D, S, c = convert_order_data(order_data)
    print(D,S,c)

    # Initialize model builder and solver based on the model type
    if model_type == 'Gurobi':
        model_builder = GurobiModel()
        solver = GurobiSolver(model_builder.model)
    elif model_type == 'Pulp':
        model_builder = PulpModel()
        solver = PulpSolver(model_builder)
    elif model_type == 'GA':
        model_builder = GeneticAlgorithmModel()
        total_demand = sum(D.values())
        model_builder.build_model(c.values(), sum(D.values()))  # Here, assuming you want to minimize the cost
        solver = GASolver(model_builder.ga_instance)
    else:
        print(f"Invalid model type: {model_type}")
        return

    # Build and solve the model
    if model_type != 'GA':                       
        model_builder.build_model(D, S, c)
    solution = solver.solve_model()

    print(f"Solution for {model_type}: ", solution)
    return solution


if __name__ == "__main__":
    app.run(debug=True)
---

This is the what other ask me to do :  
 

1，接口要求（脱密转换）

接口名称：getZytpcl

接口功能：根据商品订单生成最优仓库调配推荐

请求方式：POST

请求参数：List<Spdd>
商品订单 必填

spmzd
商品满足度 选填（缺省100%）

dpsx 调配顺序
选填（缺省是从远处仓库先调货）

Spdd实体类字段

String
ddnm 订单内码

String
qynm 提交商品订单企业内码(通过企业内码可以查询企业所在地进一步确定所在网盒)

String
spnm 商品内码

String sl
商品数量

lg 量纲

Date
zwdpwcsj最晚商品调配完成时间

二、约束条件

1 仓库供应顺序

从最远仓库开始运或者从最近仓库开始运（例如对时间要求高的商品是就近仓库发货，时间要求不高的商品是从远处仓库发货）

2.商品满足度

供应商品的满足程度
比如一个订单需要100个西瓜，满足度为80% 那么只配送80个就算完成这个订单

三、输入输出

1.输入

排序好的商品订单集合

商品满足度

调配顺序

2.输出

最优仓库调配推荐



这是梳理出来的对算法接口和约束条件的要求，你们看一下，是否有看不懂的地方，需要当面沟通就约一下时间，尽快沟通，如果在6号哪个条件实现不了，就提出来沟通一下看看是否能放到下一个版本，因为需求他们是5月底就定好了的。

---  

here is the final prompt for you:  
your goal is to help me to accomplish the customer's request, which i have done 
some of the request.
the first subtask 
is to give me a detailed todolist , show what is done and what is not.
 For every item
in not done todolist, gen prompts for each
of them so that i can reach the goal by typing those
prompts one by one to GPT4,
```
