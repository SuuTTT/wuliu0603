# api.py
import requests
import json
import pulp
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_warehouse_costs(order):
    url = 'http://localhost:8000/sptp/queryYscb'  
    payload = {
        "cknm": order["cknm"], 
        "pfwhnm": order["pfwhnm"]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error in get_warehouse_costs: {response.status_code}, {response.text}")

def get_warehouse_stocks(order, ckdata):
    print("in get_warehouse_stocks------------")
    url = 'http://localhost:8000/sptp/ckylcxByUTC'
    payload = {
        "cknm": ckdata["cknm"],
        "spnm": order["spnm"],
        "zwdpwcsj": order["zwdpwcsj"]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(f"Error in get_warehouse_stocks: {response.status_code}, {response.text}")

@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    req = request.json

    # Creating a LP problem
    prob = pulp.LpProblem("Warehouse_Distribution_Problem", pulp.LpMinimize)

    # Creating decision variables
    x = pulp.LpVariable.dicts("x", ((i, j, n) for i in range(len(req["Spdd"])) for j in range(len(req["Spdd"][i]["ckdata"])) for n in range(len(req["Spdd"][i]["spnm"]))), lowBound=0, cat='Integer')

    # Creating objective function: minimize total cost
    prob += pulp.lpSum(req["Spdd"][i]["ckdata"][j]["yscb"] * x[i, j, n] for i in range(len(req["Spdd"])) for j in range(len(req["Spdd"][i]["ckdata"])) for n in range(len(req["Spdd"][i]["spnm"])))

    # Adding constraints: each order's demand must be satisfied to a certain degree
    for i in range(len(req["Spdd"])):
        for n in range(len(req["Spdd"][i]["spnm"])):
            prob += pulp.lpSum(x[i, j, n] for j in range(len(req["Spdd"][i]["ckdata"]))) >= req["Spdd"][i]["sl"] * req["spmzd"]

    # Adding constraints: warehouse can't allocate more than its available stock
        for i in range(len(req["Spdd"])):
            for j in range(len(req["Spdd"][i]["ckdata"])):
                for n in range(len(req["Spdd"][i]["spnm"])):
                    # Getting the stocks from the mock API for the specific product and warehouse
                    stocks_list = get_warehouse_stocks(req["Spdd"][i], req["Spdd"][i]["ckdata"][j])

                    # Iterating through the list of stocks
                    for stocks in stocks_list:
                        # Finding the corresponding stock quantity for the current product
                        for stock in stocks["data"]:
                            if req["Spdd"][i]["spnm"][n] == stock['spnm']:
                                warehouse_stocks = sum([wh['xyl'] for wh in stock['ckkcsjVOS'][0]['ckkcvos']])
                                prob += pulp.lpSum(x[k, j, n] for k in range(len(req["Spdd"]))) <= warehouse_stocks

print(prob)

    print(prob)

    # Solving the problem
    prob.solve()

    # Checking the solution status
    if pulp.LpStatus[prob.status] != 'Optimal':
        return jsonify({"error": "No optimal solution found."})

    # Creating a list to store the results
    results = []
    for i in range(len(req["Spdd"])):
        for j in range(len(req["Spdd"][i]["ckdata"])):
            for n in range(len(req["Spdd"][i]["spnm"])):
                if x[i, j, n].varValue > 0:
                    results.append({
                        "cknm": req["Spdd"][i]["ckdata"][j]["cknm"],
                        "qynm": req["Spdd"][i]["qynm"],
                        "spnm": req["Spdd"][i]["spnm"][n],
                        "xqsj": req["Spdd"][i]["zwdpwcsj"],
                        "cb": req["Spdd"][i]["ckdata"][j]["yscb"] * x[i, j, n].varValue
                    })

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
