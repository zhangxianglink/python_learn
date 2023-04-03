# -*- coding: utf-8 -*-
class MyStuff(object):
    def __init__(self):
        self.msg = "init a element "

    def apple(self):
        print("eat a apple")


stuff = MyStuff()
print(stuff.msg)
stuff.apple()


class MyLoop(object):
    def __init__(self, arr):
        self.arr = arr
    def foreach(self):
        for i in self.arr:
            print(i)


word=["----","6666666","******","@@@@@@","!!!!!!"]
MyLoop(word).foreach()