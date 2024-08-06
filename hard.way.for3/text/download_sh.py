# -*- coding: utf-8 -*-

import requests
import os
import pandas as pd

# 读取Excel文件
df = pd.read_excel('D:\\data\\yy6\\待分析录音.xlsx')

# 指定下载文件夹路径
download_folder = 'D:\\data\\yy6\\audio'

# 遍历Excel中的每一行
for i in range(len(df)):
    download_url = df.iloc[i]['录音地址'].replace(" ", "")
    filename = download_url.split('/')[-1]  # 从URL中获取文件名
    filePath = os.path.join(download_folder, filename)   # 构建文件保存路径

    try:
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()
        with open(filePath, "wb") as f:
            f.write(response.content)
        print("成功下载文件：" + filePath)

    except requests.exceptions.RequestException as e:
        print("下载文件失败：" + filePath)


