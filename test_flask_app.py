# test_flask_app.py
import requests
import json

# Sample data for testing
data = [
    {"ddnm": "order1", "qynm": "company1", "spnm": 0, "sl": 10, "lg": "pcs", "zwdpwcsj": "2023-06-06"},
    {"ddnm": "order2", "qynm": "company2", "spnm": 0, "sl": 5, "lg": "pcs", "zwdpwcsj": "2023-06-07"}
]

# Convert list to json
data_json = json.dumps(data)

# Headers
headers = {'Content-type': 'application/json'}

response = requests.post('http://127.0.0.1:5000/getZytpcl', data=data_json, headers=headers)

print(response.text)
