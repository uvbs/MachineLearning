import numpy as np

f = open("data.txt", "wr")
b = [np.random.rand() * 10 for i in range(200)]
for i in b:
    f.write("%.02f %.02f\n" % (float(i), (float(i)+np.random.rand()) ** 2))
f.close()
