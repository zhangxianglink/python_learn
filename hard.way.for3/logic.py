a = input("变量a: ")
b = input("变量b: ")
if a > b:
    print(f"{a} > {b}")
elif a < b:
    print(f"{a} < {b}")
else:
    print(f"{a} == {b}")


def jo():
    c = {"status_code": 200, "result": "ok", "message": "错误"}
    if c != 200:
        print("200--------------")
    else:
        print("ok -------------")
    print(c["message"])


if __name__ == "__main__":
    jo()
