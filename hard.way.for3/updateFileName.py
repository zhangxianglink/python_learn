import os
import re


def replace_space(directory):
    for filename in os.listdir(directory):
        # 获取文件的绝对路径
        filepath = os.path.join(directory, filename)

        # 检查文件是否为目录
        if os.path.isdir(filepath):
            replace_space(filepath)  # 递归调用处理子目录
        else:
            # 替换文件中的空
            new_filename = re.sub(r'\s+', '_', filename)

            # 构造新的文件路径
            new_filepath = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(filepath, new_filepath)


# 指定目录
directory = 'D:\\app\\短信拒绝原因文件'

# 调用函数替换文件名中的空格
replace_space(directory)
