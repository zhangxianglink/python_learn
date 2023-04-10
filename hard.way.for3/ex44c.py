# -*- coding: utf-8 -*-
class Parent(object):
    def __init__(self,name):
        print(name)
    def oo(self):
        print("p oo ------------")


class Son(Parent):
    def __init__(self):
        super(Son,self).__init__("son init parent")
    def oo(self):
        print("c oo ------------")
        super(Son,self).oo()


p = Parent("parent init")
c = Son()
c.oo()