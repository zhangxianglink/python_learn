# -*- coding: utf-8 -*-
from logic_loop import show
s1 = {1, 3, 5, 6, 7}
s2 = {3, 4, 5, 6}

print(s2.intersection(s1))

print(s1.difference(s2).union(s2.difference(s1)))

print(s1.symmetric_difference(s2))

person = {
    'first_name': 'Asabeneh',
    'last_name': 'Yetayeh',
    'age': 250,
    'country': 'Finland',
    'is_marred': True,
    'skills': ['JavaScript', 'React', 'Node', 'MongoDB', 'Python'],
    'address': {
        'street': 'Space street',
        'zipcode': '02210'
    }
}

city = person.get('city')
if city is None:
    print("ye, not found")


a = 3
print('A is positive') if a > 0 else print('A is negative')

print(show(1,2))