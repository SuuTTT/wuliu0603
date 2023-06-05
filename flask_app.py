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
