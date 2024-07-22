# -*- coding: utf-8 -*-
import requests
import json
# 模型重启

payload1 = json.dumps({
  "choice": 0,
  "port": 8081
})
payload2 = json.dumps({
  "choice": 1,
  "port": 8082
})
payload3 = json.dumps({
  "choice": 0,
  "port": 8082
})
payload4 = json.dumps({
  "choice": 1,
  "port": 8083
})

headers = {
  'Content-Type': 'application/json'
}

response1 = requests.request("POST", "http://192.168.1.106:8009/run_script", headers=headers, data=payload3)
print(response1.text)
response2 = requests.request("POST", "http://192.168.1.106:8009/run_script", headers=headers, data=payload4)
print(response2.text)
response3 = requests.request("POST", "http://192.168.2.104:8009/run_script", headers=headers, data=payload1)
print(response3.text)
response4 = requests.request("POST", "http://192.168.2.104:8009/run_script", headers=headers, data=payload2)
print(response4.text)
response5 = requests.request("POST", "http://192.168.2.117:8009/run_script", headers=headers, data=payload1)
print(response5.text)
response6 = requests.request("POST", "http://192.168.2.117:8009/run_script", headers=headers, data=payload2)
print(response6.text)
response7 = requests.request("POST", "http://192.168.2.23:8009/run_script", headers=headers, data=payload1)
print(response7.text)
response8 = requests.request("POST", "http://192.168.2.23:8009/run_script", headers=headers, data=payload2)
print(response8.text)

response9 = requests.request("POST", "http://192.168.2.45:8009/run_script", headers=headers, data=payload1)
print(response9.text)
response10 = requests.request("POST", "http://192.168.2.45:8009/run_script", headers=headers, data=payload2)
print(response10.text)
response11 = requests.request("POST", "http://192.168.2.9:8009/run_script", headers=headers, data=payload1)
print(response11.text)
response12 = requests.request("POST", "http://192.168.2.9:8009/run_script", headers=headers, data=payload2)
print(response12.text)
response13 = requests.request("POST", "http://192.168.2.99:8009/run_script", headers=headers, data=payload1)
print(response13.text)
response14 = requests.request("POST", "http://192.168.2.99:8009/run_script", headers=headers, data=payload2)
print(response14.text)

response15 = requests.request("POST", "http://192.168.2.71:8009/run_script", headers=headers, data=payload1)
print(response15.text)
response16 = requests.request("POST", "http://192.168.2.72:8009/run_script", headers=headers, data=payload1)
print(response16.text)
response17 = requests.request("POST", "http://192.168.2.8:8009/run_script", headers=headers, data=payload1)
print(response17.text)
response18 = requests.request("POST", "http://192.168.2.89:8009/run_script", headers=headers, data=payload1)
print(response18.text)