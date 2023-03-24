ten_things = "Apples Oranges Crows Telephone Light Sugar"
more_stuff = ["Day", "Night", "Song", "Frisbee", "Corn", "Banana", "Girl", "Boy"]
stuff = ten_things.split(' ')

while len(stuff) != 10:
    next = more_stuff.pop()
    print("next ",next)
    stuff.append(next)
    print(f"There are {len(stuff)} items now.")


print("there is my stuff", stuff)

print(stuff[0])
print(stuff[-1])
print(','.join(stuff))
print('#'.join(stuff[3:5]))