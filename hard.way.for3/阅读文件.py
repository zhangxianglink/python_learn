from sys import argv

script, filename = argv

txt  = open(filename)

print(f"this is your file: {filename};")
print(txt.read())

print(f"读取文件： ")
file_again = input("> ")

txt_again = open(file_again)
print(txt_again.read())

txt_again.close()
txt.close()