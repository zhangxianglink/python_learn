# -*- coding: utf-8 -*-
import openpyxl
import json

workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.append(["Output", "Input", "Instruction"])
with open("D:\\data\\models\\f.txt", "r", encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)
        output = data.get("output", "")
        input_value = data.get("input", "")
        instruction = data.get("instruction", "")
        sheet.append([output, input_value, instruction])
workbook.save("D:\\data\\models\\0530.xlsx")

