from sys import argv
from os.path import exists

script, from_file, to_file = argv

print(f"Copying from {from_file} to {to_file}")

in_file = open(from_file)
indata = in_file.read()

print(f"this input file {len(indata)} bytes long")

print(f"the output file : {exists(to_file)}")
print("ready, hit return to continue, CTRL + C abort.")
input()

out_file = open(to_file, 'w')
out_file.write(indata)

print("ok,clone")
out_file.close()
in_file.close()

