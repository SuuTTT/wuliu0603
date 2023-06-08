# Import necessary modules
import json
import requests

# Read your input data
data = {
   "Spdd":[
      {
         "ddnm": "1",
         "qynm": "123",
         "spnm": "A",
         "sl": 5,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      },
      {
         "ddnm": "2",
         "qynm": "456",
         "spnm": "B",
         "sl": 3,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      },
      {
         "ddnm": "3",
         "qynm": "789",
         "spnm": "A",
         "sl": 7,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      },
      {
         "ddnm": "4",
         "qynm": "012",
         "spnm": "B",
         "sl": 2,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      },
      {
         "ddnm": "5",
         "qynm": "345",
         "spnm": "A",
         "sl": 6,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      },
      {
         "ddnm": "6",
         "qynm": "678",
         "spnm": "B",
         "sl": 1,
         "lg": "个",
         "zwdpwcsj": "2023-06-30T00:00:00",
         "jd": 39.913818,
         "wd": 116.363625,
         "ckdata": [
            {
               "cknm":"WH1",
               "pfwhnm":"BOX1",
               "yscb": 2.0
            },
            {
               "cknm":"WH2",
               "pfwhnm":"BOX2",
               "yscb": 1.0
            }
         ]
      }
   ],
   "spmzd": 0.95,
   "dpsx": "先进先出"
}



# Order count and warehouse count
num_orders = len(data["Spdd"])
num_warehouses = len(data["Spdd"][0]["ckdata"])

# Get the satisfaction rate
satisfaction = data["spmzd"]

# Parsing the order information
orders = []
for order in data["Spdd"]:
    order_info = {
        "order_id": order["ddnm"],
        "product": order["spnm"],
        "quantity": order["sl"],
        "due_date": order["zwdpwcsj"],
        "warehouses": {wh["cknm"]: wh["yscb"] for wh in order["ckdata"]}
    }
    orders.append(order_info)

# Parsing the warehouse information
warehouses = {}
for product in data["Spdd"][0]["ckdata"]:
    warehouses[product["cknm"]] = {}

# Get the warehouse stock
response = requests.post('http://localhost:8000/ckylcxByUTC', json={})
warehouse_data = response.json()["data"]
for warehouse_info in warehouse_data:
    product = warehouse_info["spnm"]
    for warehouse in warehouse_info["ckkcsjVOS"][0]["ckkcvos"]:
        warehouse_id = warehouse["cknm"]
        quantity = warehouse["xyl"]
        warehouses[warehouse_id][product] = quantity

# Transform the information to text description
description = f"We assume we have {num_orders} orders and {num_warehouses} warehouses, each order only needs one kind of product, and each warehouse has these two products. The detailed information of orders and warehouses is as follows:\n\nOrder information:\n\n"

for order in orders:
    description += f"- Order {order['order_id']}: need product {order['product']} {order['quantity']} units, the latest completion time is {order['due_date']}.\n"

description += "\nWarehouse information:\n\n"

for warehouse_id, warehouse_info in warehouses.items():
    description += f"- Warehouse {warehouse_id}: have product A {warehouse_info.get('A', 0)} units, product B {warehouse_info.get('B', 0)} units, the transportation cost is {orders[0]['warehouses'][warehouse_id]} yuan per unit.\n"

description += f"\nThe satisfaction requirement is {int(satisfaction*100)}%, that is, each order only needs to satisfy {int(satisfaction*100)}% of the product demand."

print(description)
