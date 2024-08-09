# -*- coding: utf-8 -*-
import pandas as pd
import mysql.connector

# 读取 Excel 文件
df = pd.read_excel("C:\\Users\\admin\\Desktop\\标数\\0807\\入库数据.xlsx")

# 数据库连接配置
db_config = {
    'user': 'root',
    'password': 'cyaiyc',
    'host': 'localhost',
    'database': 'cydb2'
}

# 连接到 MySQL 数据库
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 假设 train_data 表的列名与 Excel 文件中的列名相同
table_name = 'train_data'

# 生成插入 SQL 语句
columns = ', '.join(df.columns)
placeholders = ', '.join(['%s'] * len(df.columns))  # 为参数化查询生成占位符
sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

# 执行插入操作
for index, row in df.iterrows():
    # 将数据转换为元组
    data = tuple(row.fillna(value=pd.NA))  # 替换 NaN 为 None
    cursor.execute(sql, data)

# 提交事务并关闭连接
conn.commit()
cursor.close()
conn.close()
