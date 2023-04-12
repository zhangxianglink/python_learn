# -*- coding: utf-8 -*-
import os
from pandas import DataFrame
from sys import argv
script,file_path = argv

print(" 递归 ------------------  ")
for root,dirs,files in os.walk(file_path):
    print(f"根目录 ${root},文件夹 ${dirs},文件 ${files}")

print(" 非递归 ------------------  ")
for x in os.listdir(file_path):
    print(x)

df = DataFrame(os.listdir(file_path))
df.to_excel("C:\\Users\\admin\\Desktop\\test\\audio-recorder-master\\new.xlsx")