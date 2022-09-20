import random

a = int(input())
b = int(input())


with open("output.txt", "w") as file:
    file.write(str(a+b))