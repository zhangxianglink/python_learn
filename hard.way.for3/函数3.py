# -*- coding: utf-8 -*-

from sys import argv
script, input_file = argv

def _print_all(f):
    print(f.read())

# 重置到第0个字节
def rewind(f):
    f.seek(0)

def print_a_line(line_count,f):
    print(line_count, f.readline())

current_file = open(input_file)
_print_all(current_file)
print("\n")
rewind(current_file)
print_a_line(3,current_file)