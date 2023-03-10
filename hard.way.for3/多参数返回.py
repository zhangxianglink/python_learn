# -*- coding: utf-8 -*-
from ex25 import *

def secret_formula(started):
    a = started * 500
    b = a / 20
    c = b / 100
    return a, b, c

_a, _b , _c = secret_formula(10000)

print(f"a : {_a} ,b: {_b}, c : {_c}")



# run ex25
print("break_words: {}".format(break_words(" 1  1   2       3")))
print("sort_words: {}".format(sort_words("a321b")))
arr = ["走","🐻"]
print("print_first_word: {}".format(print_first_word(arr)))
print("print_last_word: {}".format(print_last_word(arr)))

