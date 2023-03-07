# coding=UTF-8
from sys import argv

script, filename = argv

target = open(filename, 'w')
target.truncate()

line1 = input("line 1: ")
line2 = input("line 2: ")
line3 = input("line 3: ")

target.write(line1+"\n")
target.write(line2+"\n")
target.write(line3+"\n")

target.close()