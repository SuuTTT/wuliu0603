from flask import Flask, request, jsonify
import operator

# 我对数据格式的假设包括：

# 1. **订单信息（`Spdd`）**：假设订单信息是一个包含字典的列表。每个字典代表一个订单，包含商品内码（`spnm`）和商品数量（`sl`）。这意味着每个订单只包含一种商品。如果一个订单可以包含多种商品，那么这个格式可能需要进行调整。

# 2. **商品满足度（`spmzd`）**：假设商品满足度是一个0到100之间的整数，代表订单的满足程度。如果满足度可以是一个小数，或者使用其他的表示方式，那么这个假设可能需要进行调整。

# 3. **调配顺序（`dpsx`）**：假设调配顺序是一个字符串，可以是`FAR_FIRST`（从最远的仓库开始）或`NEAR_FIRST`（从最近的仓库开始）。如果调配顺序有其他的可能值，或者使用其他的表示方式，那么这个假设可能需要进行调整。

# 4. **仓库库存数据**：在示例代码中，我假设仓库库存数据是一个字典，其中的键是仓库内码，值是另一个字典，表示该仓库的库存情况。这个内部字典的键是商品内码，值是该商品的库存量。如果实际的仓库库存数据的格式不同，那么这个假设可能需要进行调整。

# 我还做了以下的简化假设：

# 1. **所有仓库都可以调配所有商品**：在`warehouse_data`字典中，我假设所有的仓库都可以调配所有的商品。这可能不符合实际情况，因为一些仓库可能没有某些商品的库存。

# 2. **调配成本是一个固定的比例**：在计算调配成本时，我假设调配成本是数量的10倍。这只是一个简化的假设，实际的调配成本可能会根据很多因素变化，例如距离、运输方式等。

# 3. **仓库库存数据是固定的**：在这个示例代码中，我假设仓库的库存数据是固定的，并且直接在代码中定义了一个`warehouse_data`字典。在实际情况中，仓库的库存数据可能会经常变化，并且应该从数据库或其他数据源获取。

# 4. **企业内码和需求时间是固定的**：在生成返回结果时，我使用了"example_qynm"和"example_xqsj"作为企业内码和需求时间。这只是一个简化的假设，实际的企业内码和需求时间应该从请求参数或其他数据源获取。

# 5. **没有实现复杂的调配算法**：在这个示例代码中，我使用了一个简单的调配算法：按照调配顺序依次满足每个订单的需求，直到仓库的库存量不足。这个算法可能不能得到最优的调配方案，但是它简单且易于实现。

# 6. **没有处理错误和异常**：在这个示例代码中，我没有处理可能出现的错误和异常，例如请求参数的格式错误、仓库库存不足等。在实际的代码中，应该添加适当的错误处理和异常处理代码，以确保接口的稳定性和可靠性。


app = Flask(__name__)

# 模拟的仓库库存数据，实际情况中应从数据库或其他数据源获取
warehouse_data = {
    "warehouse1": {"apple": 100, "banana": 200},
    "warehouse2": {"apple": 150, "banana": 250}
}

@app.route('/getZytpcl', methods=['POST'])
def get_zytpcl():
    data = request.get_json()

    # 解析请求参数
    spdd = data.get('Spdd', [])
    spmzd = data.get('spmzd', 0)
    dpsx = data.get('dpsx', '')

    # 验证请求参数
    if not spdd or not isinstance(spdd, list):
        return jsonify({"error": "Invalid Spdd"}), 400
    if not isinstance(spmzd, int) or spmzd < 0 or spmzd > 100:
        return jsonify({"error": "Invalid spmzd"}), 400
    if dpsx not in ['FAR_FIRST', 'NEAR_FIRST']:
        return jsonify({"error": "Invalid dpsx"}), 400

    # 计算订单需求量
    orders = []
    for order in spdd:
        spnm = order.get('spnm')
        sl = order.get('sl', 0)
        demand = sl * spmzd // 100
        orders.append((spnm, demand))

    # 排序订单
    if dpsx == 'FAR_FIRST':
        orders.sort(key=operator.itemgetter(1), reverse=True)
    else:
        orders.sort(key=operator.itemgetter(1))

    # 调配算法
    results = []
    for spnm, demand in orders:
        for warehouse, inventory in warehouse_data.items():
            if inventory.get(spnm, 0) >= demand:
                inventory[spnm] -= demand
                results.append({
                    "cknm": warehouse,
                    "qynm": "example_qynm",
                    "spnm": spnm,
                    "xqsj": "example_xqsj",
                    "cb": demand * 10  # 假设调配成本为数量*10
                })
                break

    # 返回结果
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
