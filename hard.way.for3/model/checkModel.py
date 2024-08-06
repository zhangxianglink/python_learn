# -*- coding: utf-8 -*-
import requests
import pandas as pd

url = "http://192.168.2.68:8082/v1/chat/user_profile_half2"

headers = {
  'Content-Type': 'application/json'
}

df = pd.read_excel('D:\\data\\yy6\\h2_425.xlsx')


# 转换为JSON格式
for i in range(len(df)):
    data = df.iloc[i]['data']
    phone = df.iloc[i]['phone']
    print(phone)
    jsonData = {"stream":False,"model":"Qwen2-7b","audio_text": data}
    response = requests.post(url, json=jsonData)
    text = response.text
    print(text)






