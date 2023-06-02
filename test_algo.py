from data_read_module.data_reader import DataReader
from optimization_model_module.model_builder import GurobiModel, PulpModel, GeneticAlgorithmModel
from optimization_solver_module.solver import GurobiSolver, PulpSolver, GASolver

import pandas as pd

def test_data_reader():
    # Initialize DataReader
    data_reader = DataReader("root", "qwe123", "localhost", "wuliu")

    # Table names for testing
    tables = ['Grid', 'User', 'Product', 'Warehouse', 'WarehouseProduct', 'Transportation', 'TransportationProduct', 'Demand', 'DemandProduct']

    # Read data from each table
    data_dict = {}
    for table in tables:
        data = data_reader.read_data(table)
        assert isinstance(data, pd.DataFrame)
        print(f"Data from {table}:", data.head())
        data_dict[table] = data

    return data_dict

def test_model_builder_and_solver(model_type):
    # Read test data
    data_dict = test_data_reader()

    # Create a dictionary with demand and supply data from test data
    D = data_dict['DemandProduct']['Quantity'].to_dict()
    S = data_dict['WarehouseProduct']['Stock'].to_dict()

    # Create cost dictionary from test data
    c = data_dict['TransportationProduct']['Quantity'].to_dict()  # Assuming transportation product quantity as cost

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



# Test all model types
for model_type in ['GA','Gurobi', 'Pulp' ]:
    test_model_builder_and_solver(model_type)



