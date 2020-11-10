from numpy import random

z = 0
o = 0
t = 0
temp = []
for j in range(100000):
    size = 2
    i = random.randint(size)
    if i == 0:
        z += 1
    elif i == 1:
        o += 1
    elif i == 2:
        t += 1
    else:
        temp.append(i)
print(z, o, t, temp)
