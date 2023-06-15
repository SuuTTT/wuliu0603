#api_test.py
import requests
import json

url = "http://localhost:8080/getZytpcl"

data = {
   "Spdd":[
      {
         "ddnm": "1",
         "qynm": "123",
         "spnm": "AUX",
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
         "spnm": "BUCKER",
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

given_data={
	"spmzd":"95",
	"Spdd":[
		{
			"ddnm":"01",
			"qynm":"qynm1",
			"zwdpwcsj":"2023-06-290T00:00:00",
			"spnm":"01",
			"sl":"230",
			"lg":"个"
		},
		{
			"ddnm":"02",
			"qynm":"qynm2",
			"zwdpwcsj":"2023-06-30T00:00:00",
			"spnm":"02",
			"sl":"130",
			"lg":"个"
		}
	],
	"dpsx":"调配顺序"
}
data=given_data
headers = {'Content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

try:
    print(response.json())
except json.JSONDecodeError:
    print("Empty response, no JSON to decode")

