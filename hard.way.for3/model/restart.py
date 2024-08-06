# -*- coding: utf-8 -*-
import requests
import json
import time
# 模型重启

payload1 = json.dumps({
  "type": "restart",
  "port": 8081
})
payload2 = json.dumps({
  "type": "restart",
  "port": 8082
})

headers = {
  'Content-Type': 'application/json'
}

# urls = [
# #     "http://192.168.2.58:8009/run_script",
# #     "http://192.168.2.20:8009/run_script",
# #     "http://192.168.2.68:8009/run_script",
#     "http://192.168.2.23:8009/run_script"
# ]


urls = [
    "http://192.168.2.117:8009/run_script",
    "http://192.168.2.104:8009/run_script",
    "http://192.168.2.45:8009/run_script",
    "http://192.168.2.99:8009/run_script",
    "http://192.168.2.72:8009/run_script",
    "http://192.168.2.71:8009/run_script",
    "http://192.168.2.9:8009/run_script",
    "http://192.168.1.106:8009/run_script",
    "http://192.168.2.8:8009/run_script",
    "http://192.168.2.89:8009/run_script"
]

for url in urls:
  response = requests.request("POST", url, headers=headers, data=payload1)
  print(response.text)

time.sleep(20)

for url in urls:
  response2 = requests.request("POST", url, headers=headers, data=payload2)
  print(response2.text)
