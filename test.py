# import matplotlib.pyplot as plt
# import numpy as np
#
# gradient = np.linspace(0, 1, 256)
# print(np.shape(gradient))
# print(np.shape(gradient.reshape((-1, 1))))
# gradient = gradient * gradient.reshape((-1, 1))
# print(np.shape(gradient))
#
# fig = plt.figure()
# CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
#                   vmax=zmax, vmin=zmin)
# plt.colorbar()
# plt.show()

f = open("help.txt", "w")
f.write("hellow world")
f.write(str(5))
