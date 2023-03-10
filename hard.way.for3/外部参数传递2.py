from sys import argv

script, user_name = argv
prompt = ' > '

print(f"{user_name} , {script}")
likes = input(prompt)
computer = input(prompt)
lives = input(prompt)

print(f"""
{likes}
{computer}
{lives}
""")