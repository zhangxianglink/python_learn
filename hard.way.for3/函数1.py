import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('C:\\Users\\admin\\Desktop\\标数\\对比0627.xlsx')

result = {}

# 遍历每一行数据
for index, row in df.iterrows():
    # 解析第二列和第三列的JSON数据
    json_data_col2 = json.loads(row.iloc[1])
    json_data_col3 = json.loads(row.iloc[2])
    map = dict(json_data_col3.items())
    # 遍历第二列的JSON数据
    for key, value in json_data_col2.items():
        v2 = map[key]
        if value[0] == v2[0]:
            if key in result:
                result[key] = result[key] + 1
            else:
                result[key] = 1

print(result)

