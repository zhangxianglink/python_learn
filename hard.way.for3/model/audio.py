# -*- coding: utf-8 -*-
import requests
import pandas as pd
import openpyxl
import json

# 读取Excel文件
df = pd.read_excel("C:\\Users\\admin\\Desktop\\过程声纹test.xlsx")

results = "["
# 创建一个新的excel文件
workbook = openpyxl.Workbook()
sheet = workbook.active
count = 1
for i in range(len(df)):
    audio_test = df.iloc[i]['audio_test']
    dist = df.iloc[i]['dist']
    audio_testdb = df.iloc[i]['user_id']
    if 'http' not in audio_test and '_' in audio_test:
        url = f"http://192.168.2.4:10005/voicetest/?audio_path1=/nas_data1/audio_test/{audio_test}&audio_path2=/nas_data1/audio_testdb/{audio_testdb}.wav"
        payload = ""
        headers = {}
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = response.text
            print(f"{count},{audio_test},{audio_testdb} - {result}")

            row = {
                'audio_test': audio_test,
                'user_id': str(audio_testdb),
                'dist': result
            }
            json_str = json.dumps(row, ensure_ascii=False) + ",\n"
            results += json_str
        except Exception as e:
            print(e)
            print(f"Error{count},{audio_test}")
        count += 1

results += "]"
# 写入txt文件
with open('C:\\Users\\admin\\Desktop\\过程声纹.json', 'w', encoding='utf-8') as file:
    file.write(results)
