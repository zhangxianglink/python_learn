# -*- coding: utf-8 -*-
formatter = "{} {} {} {}"

print(formatter.format(1, 2, 3, 4))
print(formatter.format(True, False, ImportError, 0.2))
print(formatter.format(formatter, formatter, formatter, formatter))

print(formatter.format(
    "this is ",
    "my favorite ",
    "soccer player",
    "梅西"
))

day = "1\n2\n3\n4\n5\n6\n7"
print(day)
print("""-----------------
I want to take a vacation.
where ? japan or france
""")

tabby_cat = "\tI'm tabbed in;"
persian_cat = "I'm split\non a line."
backslash_cat = "I'm \\ a \\ cat."

fat_cat = """
I'll do a list:
\t* cat food
\t* Fish
\t* ken \n\t* soccer
"""

print(tabby_cat)
print(persian_cat)
print(backslash_cat)
print(fat_cat)












