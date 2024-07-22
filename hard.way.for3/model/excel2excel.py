# -*- coding: utf-8 -*-
import pandas as pd
import openpyxl
import json

# 读取Excel文件
df = pd.read_excel("D:\\linuxupload\\models\\永怡画像10_half2调整版.xlsx")

# 创建一个新的excel文件
workbook = openpyxl.Workbook()
sheet = workbook.active
row = 1
for i in range(len(df)):
    half1 = df.iloc[i]['half1']
    half2_0713 = df.iloc[i]['half2-0713']
    half1_0716 = df.iloc[i]['half2-0716']
    half20713 = json.loads(half2_0713)
    half20716 = json.loads(half1_0716)
    half1j = json.loads(half1)
    print(type(half20713['data']['message']))
    a = json.loads(half20713['data']['message'])

    sheet.cell(row, 1, df.iloc[i]['入参'])
    sheet.cell(row, 2, json.dumps(a, ensure_ascii=False, indent=4))
    sheet.cell(row, 3, half20716['data']['message'] )
    sheet.cell(row, 4, half1j['data']['message'] )

    row += 1

# 保存excel文件
workbook.save("D:\\linuxupload\\models\\永怡画像10_half2调整版2.xlsx")
