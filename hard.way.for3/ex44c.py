# -*- coding: utf-8 -*-
# 你可以使用openpyxl库来读取和写入Excel文件。以下是一个示例代码，可以按顺序读取文件a的每行数据，并将数据写入到文件b的每行最后一个单元格中。

import pandas as pd

# 读取Excel文件
df = pd.read_excel('C:\\Users\\admin\\Desktop\\data0702.xlsx')

# 将数据转换为JSON格式
json_data = df.to_json(orient='records', force_ascii=False, lines=True, default_handler=str)

# 将JSON数据保存到文件中
with open('C:\\Users\\admin\\Desktop\\data0702.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

