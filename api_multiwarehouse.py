# api.py
import requests
import json
import pulp
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_total_costs(order,ckdata):
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
        raise Exception(f"Error in get_total_costs: {response.status_code}, {response.text}")


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
    req = request.json
    total_costs = []
    for i in range(len(req["Spdd"])):
        for j in range(len(req["Spdd"][i]["ckdata"])):
            total_costs.append(get_total_costs(req["Spdd"][i], req["Spdd"][i]["ckdata"][j])["data"])

    prob = pulp.LpProblem("Warehouse_Distribution_Problem", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(len(req["Spdd"])) for j in range(len(req["Spdd"][i]["ckdata"]))), lowBound=0, cat='Integer')

    prob += pulp.lpSum((req["Spdd"][i]["ckdata"][j]["yscb"] + total_costs[i]) * x[i, j] for i in range(len(req["Spdd"])) for j in range(len(req["Spdd"][i]["ckdata"])))

    for i in range(len(req["Spdd"])):
        prob += pulp.lpSum(x[i, j] for j in range(len(req["Spdd"][i]["ckdata"]))) >= req["Spdd"][i]["sl"] * req["spmzd"]

    warehouse_stocks = []
    for i in range(len(req["Spdd"])):
        stocks = get_warehouse_stocks([req["Spdd"][i]])["data"]
        warehouse_stocks.append(sum([wh['xyl'] for wh in stocks[0]['ckkcsjVOS'][0]['ckkcvos']]))

    for j in range(len(req["Spdd"][0]["ckdata"])):
        prob += pulp.lpSum(x[i, j] for i in range(len(req["Spdd"]))) <= warehouse_stocks[j]

    print(prob)
    prob.solve()

    if pulp.LpStatus[prob.status] == 'Infeasible':
        return jsonify({"code": -1, "data": {}, "message": "无推荐调配策略！"})

    results = []
    for i in range(len(req["Spdd"])):
        for j in range(len(req["Spdd"][i]["ckdata"])):
            if x[i, j].varValue > 0:
                results.append({
                    "cknm": req["Spdd"][i]["ckdata"][j]["cknm"],
                    "qynm": req["Spdd"][i]["qynm"],
                    "spnm": req["Spdd"][i]["spnm"],
                    "sl": x[i, j].varValue,
                    "lg": req["Spdd"][i]["lg"],
                    "jd": req["Spdd"][i]["jd"],
                    "wd": req["Spdd"][i]["wd"],
                    "ddnm": req["Spdd"][i]["ddnm"]
                })

    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

#result:
#(base) suu@suudeMacBook-Air wuliu0603 % python api_test.py
#[{'cknm': 'WH2', 'ddnm': '1', 'jd': 39.913818, 'lg': '个', 'qynm': '123', 'sl': 5.0, 'spnm': 'AUX', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '2', 'jd': 39.913818, 'lg': '个', 'qynm': '456', 'sl': 3.0, 'spnm': 'BUCKER', 'wd': 116.363625}, {'cknm': 'WH1', 'ddnm': '3', 'jd': 39.913818, 'lg': '个', 'qynm': '789', 'sl': 7.0, 'spnm': 'A', 'wd': 116.363625}, {'cknm': 'WH1', 'ddnm': '4', 'jd': 39.913818, 'lg': '个', 'qynm': '012', 'sl': 2.0, 'spnm': 'B', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '5', 'jd': 39.913818, 'lg': '个', 'qynm': '345', 'sl': 6.0, 'spnm': 'A', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '6', 'jd': 39.913818, 'lg': '个', 'qynm': '678', 'sl': 1.0, 'spnm': 'B', 'wd': 116.363625}]