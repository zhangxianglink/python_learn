# -*- coding: utf-8 -*-
import json
import openpyxl

# 读取json文件
with open("D:\data\dudu\\zzzzz.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

# 创建一个新的excel文件
workbook = openpyxl.Workbook()
sheet = workbook.active

# 遍历键值对并写入excel文件
row = 1
for item in data:
    output = item['output']
    input = item['data']
    instruction = item['phone']

    tff = output[0]

    sheet.cell(row, 1, input)
    sheet.cell(row, 2, instruction)
    sheet.cell(row, 3, json.dumps(tff['客户画像'], ensure_ascii=False, indent=4))
    sheet.cell(row, 4, json.dumps(tff['客户情绪'], ensure_ascii=False, indent=4))
    sheet.cell(row, 5, json.dumps(tff['客户需求'], ensure_ascii=False, indent=4))

    row += 1

# 保存excel文件
workbook.save("D:\data\dudu\\zzzzz.xlsx")

