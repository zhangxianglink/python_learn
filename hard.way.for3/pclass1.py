# -*- coding: utf-8 -*-
class MyStuff(object):
    def __init__(self):
        self.tangerine = "it is on table"

    def apple(self):
        print(f"this is a apple. {self.tangerine}")


m = MyStuff()
m.apple()
print(m.tangerine)


class Song(object):
    def __init__(self, words):
        self.words = words

    def sing(self):
        for word in self.words:
            print(word)


jay = Song(['我突然释怀的笑', '看星星一颗两颗三颗连成线', '小船'])
jay.sing()
