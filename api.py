# api.py
import requests
import json
import pulp
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)



# 获取仓库库存
def get_warehouse_stocks(dingdan):
    print("在获取仓库库存函数中------------")
    url = 'http://localhost:8000/sptp/ckylcxByUTC'
    
    # 构建商品详情信息列表
    spxqxx = []
    for order in dingdan:
        spxqxx.append({
            "spnm": order["spnm"],
            # 如果'最晚开始时间'不存在，使用'最晚调配完成时间'
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
        raise Exception(f"在获取仓库库存函数中出现错误: {response.status_code}, {response.text}")

# 获取从坐标到仓库运输商品的总成本=出库时间+运输成本+提收成本（暂时不考虑）
def get_total_costs(dingdan,ckdata):
    url = 'http://localhost:8000/sptp/queryYscb'
    payload = {
        "spnm": dingdan["spnm"],  # 商品内码
        "cknm": ckdata["cknm"],  # 仓库内码
        "jd": dingdan["jd"],  # 经度
        "wd": dingdan["wd"],  # 纬度
        "sl": dingdan["sl"],  # 商品数量
        "lg": dingdan["lg"]  # 单位
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"在获取总成本函数中出现错误: {response.status_code}, {response.text}")

@app.route("/getZytpcl", methods=['POST'])  # 获取主要调配策略
def getZytpcl():
    req = request.json  # 获取请求中的 JSON 数据

    # 获取商品订单并按最晚配送完成时间排序
    Spdd = sorted(req["Spdd"], key=lambda x: x["zwdpwcsj"])
    
    results = []  # 创建一个空列表来保存结果

    for i in range(len(Spdd)):  # 对于每个订单
        temp_order = Spdd[i].copy()  # 创建一个临时订单
        # 获取仓库数据并按运输成本排序
        ckdata = sorted(Spdd[i]["ckdata"], key=lambda x: x["yscb"])
        for j in range(len(ckdata)):  # 对于每个仓库
            # 获取仓库的库存
            warehouse_stocks = get_warehouse_stocks([temp_order])
            # 修改这里，增加商品编号（spnm）作为筛选条件
            stock = [item for data in warehouse_stocks["data"] for item in data["ckkcsjVOS"][0]["ckkcvos"] if item["cknm"] == ckdata[j]["cknm"] and data["spnm"] == temp_order["spnm"]]
            if not stock:
                continue
            stock = stock[0]
            # 如果仓库的库存能满足订单需求
            if stock["xyl"] >= temp_order["sl"]:
                total_cost = get_total_costs(temp_order, ckdata[j])  # 调用函数获取运输总成本
                results.append({  # 添加一个新的结果
                    "cknm": ckdata[j]["cknm"],  # 仓库内码
                    "qynm": temp_order["qynm"],  # 提交订单的企业ID
                    "spnm": temp_order["spnm"],  # 商品内码
                    "sl": temp_order["sl"],  # 商品数量
                    "lg": temp_order["lg"],  # 单位
                    "jd": temp_order["jd"],  # 经度
                    "wd": temp_order["wd"],  # 纬度
                    "ddnm": temp_order["ddnm"],  # 订单内码
                    "xqsj": temp_order["zwdpwcsj"],  # 添加需求时间
                    "cb": total_cost  # 添加成本
                })
                temp_order["sl"] = 0  # 清空临时订单的需求量
                break
                # ...
            else:  # 如果仓库的库存不能满足全部订单需求，分配部分商品
                temp_order["sl"] = stock["xyl"]  # 分配的数量为仓库的库存量
                total_cost = get_total_costs(temp_order, ckdata[j])  # 重新调用函数获取运输总成本
                results.append({
                    "cknm": ckdata[j]["cknm"],  # 仓库内码
                    "qynm": temp_order["qynm"],  # 提交订单的企业ID
                    "spnm": temp_order["spnm"],  # 商品内码
                    "sl": temp_order["sl"],  # 分配的数量为仓库的库存量
                    "lg": temp_order["lg"],  # 单位
                    "jd": temp_order["jd"],  # 经度
                    "wd": temp_order["wd"],  # 纬度
                    "ddnm": temp_order["ddnm"],  # 订单内码
                    "xqsj": temp_order["zwdpwcsj"],  # 添加需求时间
                    "cb": total_cost  # 添加成本
                })
                temp_order["sl"] = Spdd[i]["sl"] - stock["xyl"]  # 从临时订单的需求量中减去已分配的数量
            

        if temp_order["sl"] > 0:  # 如果临时订单的需求量还未满足，结束循环
            break
    else:  # 如果所有订单都能被满足，返回结果
        return jsonify(results)

    # 如果有订单不能被满足，返回错误信息
    return jsonify({"code": -1, "data": {}, "message": "无推荐调配策略！"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

# result
# (base) suu@suudeMacBook-Air wuliu0603 % python api_test.py
# [{'cknm': 'WH2', 'ddnm': '1', 'jd': 39.913818, 'lg': '个', 'qynm': '123', 'sl': 5.0, 'spnm': 'AUX', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '2', 'jd': 39.913818, 'lg': '个', 'qynm': '456', 'sl': 3.0, 'spnm': 'BUCKER', 'wd': 116.363625}, {'cknm': 'WH1', 'ddnm': '3', 'jd': 39.913818, 'lg': '个', 'qynm': '789', 'sl': 4.0, 'spnm': 'A', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '3', 'jd': 39.913818, 'lg': '个', 'qynm': '789', 'sl': 3.0, 'spnm': 'A', 'wd': 116.363625}, {'cknm': 'WH1', 'ddnm': '4', 'jd': 39.913818, 'lg': '个', 'qynm': '012', 'sl': 2.0, 'spnm': 'B', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '5', 'jd': 39.913818, 'lg': '个', 'qynm': '345', 'sl': 6.0, 'spnm': 'A', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '6', 'jd': 39.913818, 'lg': '个', 'qynm': '678', 'sl': 1.0, 'spnm': 'B', 'wd': 116.363625}]

# 1(base) suu@suudeMacBook-Air wuliu0603 % python api_test.py
# [{'cknm': 'WH2', 'ddnm': '1', 'jd': 39.913818, 'lg': '个', 'qynm': '123', 'sl': 5.0, 'spnm': 'AUX', 'wd': 116.363625}, {'cknm': 'WH2', 'ddnm': '6', 'jd': 39.913818, 'lg': '个', 'qynm': '678', 'sl': 7.0, 'spnm': 'B', 'wd': 116.363625}]
# (base) suu@suudeMacBook-Air wuliu0603 % 
# 2一个订单 报错。