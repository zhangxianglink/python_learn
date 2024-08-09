import pandas as pd
import json


def is_json_string(json_str):
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False


# 读取Excel文件
df = pd.read_excel("C:\\Users\\admin\\Desktop\\标数\\0807\\偏差125.xlsx")

# 转换为JSON格式
result = "["
for i in range(len(df)):
    output = df.iloc[i]['output'].replace(" ", "")
    if is_json_string(output):
        flag = df.iloc[i]['flag']
        if flag == 1:
            row = {
                'input': df.iloc[i]['input'],
                'instruction': df.iloc[i]['instruction'],
                'output': json.loads(output)
            }
            json_str = json.dumps(row, ensure_ascii=False) + ",\n"
            result += json_str
    else:
        print(output)
result += "]"

# 写入txt文件
with open("C:\\Users\\admin\\Desktop\\标数\\0807\\有诱导114.json", 'w', encoding='utf-8') as file:
    file.write(result)
