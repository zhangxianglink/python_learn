# -*- coding: utf-8 -*-
states = {
    'Oregon': 'OR',
    'Florida': 'FL',
    'California': 'CA',
    'New York': 'NY',
    'Michigan': 'MI'
}

# create a basic set of states and some cities in them
cities = {
    'CA': 'San Francisco',
    'MI': 'Detroit',
    'FL': 'Jacksonville'
}

cities['NY'] = 'New York'
cities['OR'] = 'Portland'

print('*' * 10)
print(cities['CA'])
print(states['California'])
print(cities[states['California']])

print('*' * 10)
for address,city in list(cities.items()):
    print(f"address: {address}. city: {city}")

print('*' * 10)
print(states.get("Texas"))

if not states.get("Texas"):
    print("no Texas")

city = cities.get('TX','Does Not Exist')
print(city)
