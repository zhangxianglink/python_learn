import json

# 给定的JSON结构
json_data = '''
[
    {
        "input": "a",
        "instruction": "s",
        "output": [
            {
                "编号": 14,
                "标题": "a",
                "原文摘要": "b",
                "解释": "c",
                "结果": "是"
            }
        ]
    }
]
'''

# 解析JSON数据
data = json.loads(json_data)

# 遍历output部分
for item in data:
    for output_item in item['output']:
        print("编号:", output_item['编号'])
        print("标题:", output_item['标题'])
        print("原文摘要:", output_item['原文摘要'])
        print("解释:", output_item['解释'])
        print("结果:", output_item['结果'])


# 在这个示例中，我们首先将给定的JSON结构存储在一个字符串变量json_data中。然后使用json.loads()
# 方法解析JSON数据并将其转换为Python对象。接着我们遍历output部分，打印出每个输出项中的各个字段值。
# 您可以根据实际情况修改字段名称和数据结构，以适配您的JSON数据。
