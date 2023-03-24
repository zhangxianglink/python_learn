
eyes = [1, 'brown', 2, 'blue', 3, 'green']

arr = []

for num in eyes:
    print(f"数据：{num}")

for i in range(0,6):
    print(f"range: {i}")
    arr.append(i)

for i in arr:
    print(f"arr: {i}")

for i in range(len(eyes)):
    print(f"索引：{i}，数据：{eyes[i]}")


