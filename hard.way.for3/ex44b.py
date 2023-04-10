# -*- coding: utf-8 -*-
class Parent(object):
    def pp(self):
        print("parent ________")


class Child(Parent):
    def pp(self):
        super(Child,self).pp()
        print("child _________")


p = Parent()
c = Child()
c.pp()



