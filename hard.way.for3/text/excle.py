# -*- coding: utf-8 -*-
import json
import pandas as pd

# 从文件中读取JSON数据
with open('D:\\linuxupload\\5.json' , encoding='utf-8') as f:
    data = json.load(f)

# 创建DataFrame对象
df = pd.DataFrame(data)

# 将DataFrame写入Excel文件
df.to_excel("D:\\linuxupload\\5.xlsx", index=False)
