print("嵌套测试：")
a = input(">")
if a == "1":
    print("1111111")
    b = input(">")
    if b == "2":
        print("2222222")
    if b == "3":
        print("3333333")
else:
    print("ooooooo")
    b = input(">")
    if b == "2" or b == "3":
        print("222222333333")
