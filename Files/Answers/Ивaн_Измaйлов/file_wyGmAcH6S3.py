import random

a = int(input())
b = int(input())

with open("output.txt", "w") as file:
    c = random.randint(a+b, a+b+1)
    file.write(str(c))
