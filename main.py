import serial
import time
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f = open('raw_data_J.txt', 'w')

def calc_IR_distance(reading):
    """
    This function takes an analog reading from the sensor, and converts it into
    a distance in centimeters.
    """
    # Map reading to voltage
    voltage = reading * 5 / 1023;
    # Use calibration curve to map voltage to distance
    if voltage < 0.5:
        return 0
    elif voltage < 2:
        inv_dist = (0.013 / 0.75) * voltage - (1/600)
    else:
        inv_dist = (0.034 / 0.75) * voltage - 0.0577;
    return inv_dist**(-1)

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

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2000)

# Working variables
verbose = False
tilt_range = None
pan_range = None
step_size = None
cart_coor = None
data_transmission = 0
running = True
dist_threshold = 75

# Listen for header information from the arduino
print("AWAITING HEADER INFORMATION...")
input_command = ser.readline().decode()
print(input_command)
f.write(input_command)
f.write('\n')
tilt_range, pan_range, step_size = [int(value) for value in input_command.split(',')]
tilt_samples = int(tilt_range // step_size)
pan_samples = int(pan_range // step_size)
num_samples = tilt_samples * pan_samples

cart_coor = np.zeros((3, num_samples), dtype=np.float)
sphere_coor = np.zeros((tilt_samples, pan_samples), dtype=np.float)

# Listen for the incomming data points from the arduino
while data_transmission < num_samples:
    dist = calc_IR_distance(int(ser.readline().decode()))
    f.write(str(dist) + "\n")
    if dist < dist_threshold:
        if verbose: print(dist, "---", data_transmission)

        # Back calculate corresponding tilt and pan angles based on number of transmission
        pan_index = int(data_transmission // pan_samples)
        tilt_index = int(data_transmission % pan_samples)
        theta_tilt = -(tilt_range / 2) + (step_size * tilt_index)
        phi_pan = -(pan_range / 2) + (step_size * pan_index)

        if verbose: print(theta_tilt, phi_pan, dist)

        # Store "spherical" coordinates
        sphere_coor[tilt_index][pan_index] = cart[1]

        # Convert to cartesian coordinates
        cart = calc_cart(dist, theta_tilt, phi_pan)
        for i in range(3):
            cart_coor[i][data_transmission] = cart[i]
    data_transmission += 1
    print(round(100 * data_transmission / (num_samples), 2), "% COMPLETE")

print("TRANSMISSION COMPLETE")
f.close()
ser.close()

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

fig, ax = plt.subplots()
im = ax.imshow(np.fliplr(np.flipud(sphere_coor)))
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("normal distance (cm)", rotation=-90, va="bottom")
plt.ylabel('pan angle')
plt.xlabel('tilt angle')
ax.set_xticklabels(np.arange(np.linspace(-tilt_range/2, tilt_range/2, step_size)))
ax.set_yticklabels(np.arange(np.linspace(-tilt_range/2, tilt_range/2, step_size)))

plt.show()
