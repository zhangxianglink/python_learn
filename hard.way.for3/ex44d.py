# -*- coding: utf-8 -*-
class Other(object):
    def a(self):
        print("aaaaaaaaaa")
    def b(self):
        print("bbbbbbbbbb")
    def c(self):
        print("cccccccccc")


class Obj(object):
    def __init__(self):
        self.other = Other()
    def a(self):
        self.other.a()
    def b(self):
        print("b222222222")
    def c(self):
        print("c222222222")
        self.other.c()


obj = Obj()
obj.a()
obj.b()
obj.c()
