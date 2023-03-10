# -*- coding: utf-8 -*-
def add(a, b):
    print(f"ADDING {a} + {b}")
    return a + b


def subtract(a, b):
    print(f"{a} - {b}")
    return a - b


def multiply(a, b):
    print(f"MULTIPLY {a} * {b}")
    return a * b


def divide(a, b):
    print(f"DIVIDING {a} / {b}")
    return a / b


age = add(30, 5)
height = subtract(78, 4)
weight = multiply(90, 2)
iq = divide(100, 2)

print(f"{age} , {height} , {weight} , {iq}")

what = add(age, subtract(height, multiply(weight, divide(iq, 2))))

print("That become: ", what, "Can you do it")
