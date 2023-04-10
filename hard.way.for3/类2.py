# -*- coding: utf-8 -*-
class Animal(object):
    pass


class Cat(Animal):
    def __init__(self,name):
        self.name = name


class Dog(Animal):
    def __init__(self,name):
        self.name = name


class Person(object):
    def __init__(self,name):
        self.name = name
        self.pet = None


class Employee(Person):
    def __init__(self,name,salary):
        super(Employee,self).__init__(name)
        self.salary = salary


class Fish(object):
    pass


class Salmon(Fish):
    pass


class Halibut(Fish):
    pass


dog = Dog("dog")
jack = Person("jack")
jack.pet = dog

frank = Employee("Frank", 120000)
frank.pet = dog
