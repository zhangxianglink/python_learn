# -*- coding: utf-8 -*-


class MyLoop(object):
    def __init__(self, arr):
        self.arr = arr
        self.age = 0


    def foreach(self):
        for i in self.arr:
            print(i)

    @staticmethod
    def help(s):
        print( "静态方法：" + s)

    @classmethod
    def common(cls):
        return "cls 是类对象，所有实例公用"

#   通常不需要get/set， 除非想要进行特殊处理
    @property
    def age(self):
        return self._age + 1

    # 允许属性被修改
    @age.setter
    def age(self, age):
        self._age = age + 1

    # 允许属性被删除
    @age.deleter
    def age(self):
        del self._age


if __name__ == '__main__':
    word = ["----", "6666666", "******", "@@@@@@", "!!!!!!"]
    m = MyLoop(word)
    MyLoop.help("start")
    m.age = 28
    print(m.age)
    del m.age

