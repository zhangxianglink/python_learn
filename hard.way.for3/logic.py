import json

import pandas as pd

# 读取Excel文件，假设文件名为example.xlsx
file_path = 'C:\\Users\\admin\\Desktop\\标数\\质检0702.xlsx'

# 读取Excel文件，跳过第一行
df = pd.read_excel(file_path)

first_column = df.iloc[:, 0]

for row in first_column:
    lines = row.split('\n')
    info = {
            "data": [
            ]
        }
    for line in lines:
        if len(line) == 0:
            continue
        x = {}
        parts = line.split(".")
        x["编号"] = parts[0]
        parts2 = ''.join(parts[1:]).split(":")
        x["标题"] = parts2[0]
        parts3 = ''.join(parts2[1:]).split("。")
        x["结果"] = parts3[0]
        others = ''.join(parts3[1:])
        if parts[0] == '1' or parts[0] == '4':
            x["资费"] = parts3[1]
            others = ''.join(parts3[2:])
        index1 = others.rfind("“")
        index2 = others.rfind("”")
        if index1 == -1 and index2 == -1:
            x["原文摘要"]= ""
            x["解释"] = others
        else:
            max_index = max(index1, index2) + 1
            x["原文摘要"] = others[:max_index]
            x["解释"] = others[max_index:]
        info["data"].append(x)
    json_str = json.dumps(info, ensure_ascii=False)
    print(json_str)

