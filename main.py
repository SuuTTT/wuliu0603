from data_read_module.data_reader import DataReader
from optimization_model_module.model_builder import GurobiModel, PulpModel, GeneticAlgorithmModel
from optimization_solver_module.solver import GurobiSolver, PulpSolver, GASolver

def read_data():
    # Initialize DataReader
    data_reader = DataReader("root", "qwe123", "localhost", "wuliu")

    # Table names for testing
    tables = ['Grid', 'User', 'Product', 'Warehouse', 'WarehouseProduct', 'Transportation', 'TransportationProduct', 'Demand', 'DemandProduct']

    # Read data from each table
    data_dict = {}
    for table in tables:
        data = data_reader.read_data(table)
        data_dict[table] = data

    return data_dict

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

def main():
    # Read data
    data_dict = read_data()

    # Test all model types
    #for model_type in ['GA','Gurobi', 'Pulp']:
    for model_type in ['Gurobi']:
        build_and_solve_model(data_dict, model_type)

if __name__ == "__main__":
    main()
