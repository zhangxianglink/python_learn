# -*- coding: utf-8 -*-
class Parent(object):
    def implicit(self):
        print("this is implicit.")


class Child(Parent):
    # 没有新内容定义，继承父类所有行为
    pass


p = Parent()
c = Child()

p.implicit()
c.implicit()
