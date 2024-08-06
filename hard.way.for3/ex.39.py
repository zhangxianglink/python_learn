
import pandas as pd

# 读取Excel文件
df = pd.read_excel('D:\\data\\convert16\\退订新数据-500条-2.xlsx')

# 将数据转换为JSON格式
json_data = df.to_json(orient='records', force_ascii=False, lines=True, default_handler=str)
type(json_data)

# 将JSON数据保存到文件中
with open('D:\\data\\convert16\\退订新数据-500条-2.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
