# api.py
import requests
import json
import pulp
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_warehouse_costs(order,ckdata):
    url = 'http://localhost:8000/sptp/queryYscb'
    payload = {
        "spnm": order["spnm"],
        "cknm": ckdata["cknm"],
        "jd": order["jd"],
        "wd": order["wd"],
        "sl": order["sl"],
        "lg": order["lg"]
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error in get_warehouse_costs: {response.status_code}, {response.text}")


def get_warehouse_stocks(orders):
    print("in get_warehouse_stocks------------")
    url = 'http://localhost:8000/sptp/ckylcxByUTC'
    
    # 构建spxqxx列表
    spxqxx = []
    for order in orders:
        spxqxx.append({
            "spnm": order["spnm"],
            # if 'zwkssj' is not available, use 'zwdpwcsj'
            "zwkssj": order.get("zwkssj", order["zwdpwcsj"])
        })
        
    payload = {
        "spxqxx": spxqxx
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(f"Error in get_warehouse_stocks: {response.status_code}, {response.text}")


@app.route("/getZytpcl", methods=['POST'])
def getZytpcl():
    #try:
        req = request.json
        # Before defining the LP problem, we fetch the warehouse costs.
        warehouse_costs = []
        for i in range(len(req["Spdd"])):
            for j in range(len(req["Spdd"][i]["ckdata"])):
                warehouse_costs.append(get_warehouse_costs(req["Spdd"][i], req["Spdd"][i]["ckdata"][j])["data"])

        # Creating a LP problem
        # Creating objective function: minimize total cost (including both shipping and warehouse costs)
        # ...

        # Creating a LP problem
        prob = pulp.LpProblem("Warehouse_Distribution_Problem", pulp.LpMinimize)

        # Creating decision variables
        x = pulp.LpVariable.dicts("x", ((i, j, n) for i in range(len(req["Spdd"])) for j in range(len(req["Spdd"][i]["ckdata"])) for n in range(len(req["Spdd"][i]["spnm"]))), lowBound=0, cat='Integer')

        # Creating objective function: minimize total cost
        prob += pulp.lpSum((req["Spdd"][i]["ckdata"][j]["yscb"] + warehouse_costs[i]) * x[i, j, n] for i in range(len(req["Spdd"])) for j in range(len(req["Spdd"][i]["ckdata"])) for n in range(len(req["Spdd"][i]["spnm"])))
       
        # Adding constraints: each order's demand must be satisfied to a certain degree
        for i in range(len(req["Spdd"])):
            for n in range(len(req["Spdd"][i]["spnm"])):
                prob += pulp.lpSum(x[i, j, n] for j in range(len(req["Spdd"][i]["ckdata"]))) >= req["Spdd"][i]["sl"] * req["spmzd"]

        for i in range(len(req["Spdd"])):
            # Getting the stocks from the mock API for the specific product and warehouse
            print(get_warehouse_stocks([req["Spdd"][i]]))
           
            stocks = get_warehouse_stocks([req["Spdd"][i]])["data"]
            
            for j in range(len(req["Spdd"][i]["ckdata"])):
                for n in range(len(req["Spdd"][i]["spnm"])):
                    # Finding the corresponding stock quantity for the current product
                    for stock in stocks:
                        if req["Spdd"][i]["spnm"][n] == stock['spnm']:
                            warehouse_stocks = sum([wh['xyl'] for wh in stock['ckkcsjVOS'][0]['ckkcvos']])
                            prob += pulp.lpSum(x[k, j, n] for k in range(len(req["Spdd"]))) <= warehouse_stocks




        print(prob)
        # Checking the solution status

            
        #elif pulp.LpStatus[prob.status] != 'Optimal':
        #    return jsonify({"code": 500, "data": {}, "message": "调配策略计算失败！"})

        # Solving the problem
        prob.solve()

        # Checking the solution status
        if pulp.LpStatus[prob.status] == 'Infeasible':
            return jsonify({"code": -1, "data": {}, "message": "无推荐调配策略！"})
        #elif pulp.LpStatus[prob.status] != 'Optimal':
        #    return jsonify({"code": 500, "data": {}, "message": "调配策略计算失败！"})


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
                            "sl": x[i, j, n].varValue,
                            "lg": req["Spdd"][i]["lg"],
                            #"": req["Spdd"][i]["jldw"],
                            "jd": req["Spdd"][i]["jd"],
                            "wd": req["Spdd"][i]["wd"],
                            "ddnm": req["Spdd"][i]["ddnm"]
                        })

        return jsonify(results)
    #except Exception as e:
    #    return jsonify({"code": 500, "data": {}, "message": "调配策略计算失败！"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
