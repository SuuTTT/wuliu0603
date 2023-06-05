## 在大项目中使用chatGPT的最佳实践

尽可能罗列最相关的信息，最后给出命令。

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
