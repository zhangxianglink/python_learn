# -*- coding: utf-8 -*-
def print_two(*args):
    arg1,arg2 = args
    print(f"arg1: {arg1}, arg2: {arg2}")

def print_two_again(arg1,arg2):
    print(f"arg1: {arg1}, arg2: {arg2}")

def print_one(arg1):
    print(f"arg1: {arg1}")

def print_none():
    print("no params.")

print_two("a","b")
print_two_again("a","b")
print_one("a")
print_none()