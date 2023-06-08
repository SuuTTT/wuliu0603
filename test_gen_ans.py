from pulp import *

# Problem data
orders = [
    {"id": 1, "product": "A", "quantity": 5},
    {"id": 2, "product": "B", "quantity": 3},
    {"id": 3, "product": "A", "quantity": 7},
    {"id": 4, "product": "B", "quantity": 2},
    {"id": 5, "product": "A", "quantity": 6},
    {"id": 6, "product": "B", "quantity": 1}
]
warehouses = [
    {"id": "WH1", "stock": {"A": 10, "B": 6}, "cost": 2},
    {"id": "WH2", "stock": {"A": 8, "B": 6}, "cost": 1}
]
satisfaction = 0.95

# Create a new LP problem
prob = LpProblem("Minimize Transportation Costs", LpMinimize)

# Create variables
x = LpVariable.dicts("x", [(o["id"], w["id"], p) for o in orders for w in warehouses for p in o["product"]], 0, None, LpInteger)

# Objective function
prob += lpSum([x[o["id"], w["id"], o["product"]] * w["cost"] for o in orders for w in warehouses if o["product"] in w["stock"]])

# Demand constraints
for o in orders:
    prob += lpSum([x[o["id"], w["id"], o["product"]] for w in warehouses if o["product"] in w["stock"]]) >= satisfaction * o["quantity"]

# Supply constraints
for w in warehouses:
    for p in ["A", "B"]:
        if p in w["stock"]:
            prob += lpSum([x[o["id"], w["id"], p] for o in orders if o["product"] == p]) <= w["stock"][p]

# Solve the problem
prob.solve()

# Print the optimal solution
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

print("Total cost = ", value(prob.objective))
