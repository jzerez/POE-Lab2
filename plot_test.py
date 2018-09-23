def calc_cart(radius, tilt_angle, pan_angle):
    """
    This function takes a point in spherical coordinates and expresses it in
    cartesian coordinates
    """
    z = radius * math.sin(math.radians(tilt_angle));
    radius_prime = radius * math.cos(math.radians(tilt_angle))
    y = radius_prime * math.cos(math.radians(pan_angle))
    x = radius_prime * math.sin(math.radians(pan_angle))
    return (x, y, z)
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
f = open('raw_data_J.txt', 'r')
lines = f.readlines();
tilt_range, pan_range, step_size = [int(value) for value in lines[0].split(',')]
lines = lines[2:]
tilt_samples = int(tilt_range // step_size)
pan_samples = int(pan_range // step_size)
dist_threshold = 60

cart_coor = np.zeros((3, tilt_samples * pan_samples), dtype=np.float)
sphere_coor = np.zeros((tilt_samples, pan_samples), dtype=np.float)
data_transmission = 0

for line in lines:
    if float(line) < dist_threshold:
        pan_index = int(data_transmission // pan_samples)
        tilt_index = int(data_transmission % pan_samples)
        theta_tilt = -(tilt_range / 2) + (step_size * tilt_index)
        phi_pan = -(pan_range / 2) + (step_size * pan_index)

        # Convert to cartesian coordinates
        cart = calc_cart(float(line), theta_tilt, phi_pan)
        sphere_coor[tilt_index][pan_index] = cart[1]
        for i in range(3):
            cart_coor[i][data_transmission] = cart[i]
    data_transmission += 1


# Use matplotlib to plot the points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(cart_coor[0, :], cart_coor[1, :], cart_coor[2, :], c='red')

# Attempt to set the axes to be equal to get a good aspect ratio
ax.set_aspect('equal')
ax.axis('equal')
max_dist = np.amax(cart_coor)
ax.set_xlim3d(-max_dist, max_dist)
ax.set_ylim3d(-max_dist, max_dist)
ax.set_zlim3d(-max_dist, max_dist)
plt.xlabel('X')
plt.ylabel('Y')
# plt.zlabel('Z')

fig, ax = plt.subplots()
im = ax.imshow(np.fliplr(np.flipud(sphere_coor)))
plt.xlabel('pan angle')
plt.ylabel('tilt angle')
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("normal distance (cm)", rotation=-90, va="bottom")

ax.set_xticklabels(np.arange(np.linspace(-tilt_range/2, tilt_range/2, step_size)))
ax.set_yticklabels(np.arange(np.linspace(-tilt_range/2, tilt_range/2, step_size)))

#
# plt.xticks(np.arange(np.linspace(-tilt_range/2, tilt_range/2, step_size)))
# plt.yticks(np.arange(np.linspace(-tilt_range/2, tilt_range/2, step_size)))


# CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
# vmax=zmax, vmin=zmin)
# plt.colorbar()
plt.show()
