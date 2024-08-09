# -*- coding: utf-8 -*-
import json


def split_json(start, end):
    with open("D:\\data\\convert16\\td500.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    result = []
    count = 1
    for item in data:
        if end >= count > start:
            print(count)
            result.append(item)
        count += 1;
    with open(f"D:\\data\\convert16\\td_{end}.json", 'w', encoding='utf-8') as file:
        file.write(json.dumps(result, ensure_ascii=False, indent=4))


split_json(251, 313)
split_json(313, 375)
split_json(375, 438)
split_json(438, 500)


