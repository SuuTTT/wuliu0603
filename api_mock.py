#api_mock.py
from flask import Flask, request, jsonify
import os


app = Flask(__name__)

@app.route("/sptp/queryYscb", methods=['POST'])
def mock_queryYscb():
    # 这里返回模拟数据，模拟运输成本
    return jsonify({"code": 200, "data": 36.0})

@app.route("/sptp/ckylcxByUTC", methods=['POST'])
def mock_ckylcxByUTC():
    # 这里返回模拟数据，模拟仓库库存信息
    return jsonify({
        "code": 200, 
        "data": [
            {
                "ckkcsjVOS": [ # 仓库库存时间
                    {
                        "sjjd": "2023-06-30T00:00:00",  # 时间节点
                        "ckkcvos": [
                            {
                                "cknm": "WH1",  # 仓库内码
                                "xyl": 10.0  # 现有量
                            },
                            {
                                "cknm": "WH2",  # 仓库内码
                                "xyl": 8.0  # 现有量
                            }
                        ]
                    }
                ],
                "spnm": "AUX"  # 商品内码
            },
            {
                "ckkcsjVOS": [
                    {
                        "sjjd": "2023-06-30T00:00:00",  # 时间节点
                        "ckkcvos": [
                            {
                                "cknm": "WH1",  # 仓库内码
                                "xyl": 8.0  # 现有量
                            },
                            {
                                "cknm": "WH2",  # 仓库内码
                                "xyl": 6.0  # 现有量
                            }
                        ]
                    }
                ],
                "spnm": "B"  # 商品内码
            }
        ]
    })

if __name__ == "__main__":
    app.run(port=8000,debug=True)
