# Modeling of forest fire

import numpy as np
from math import *
import forestFunc_v2 as ff
import matplotlib.pyplot as plt
import animatplot as amp
from matplotlib import animation

fig = plt.figure(figsize=(10.0, 8.0))

try:
    lattice_x = int(input('X-Lattice Size (default=100): '))
except ValueError:
    lattice_x = 100

try:
    lattice_y = int(input('Y-Lattice Size (default=60): '))
except ValueError:
    lattice_y = 60

try:
    p = float(input('Probability of Green (default=0.5): '))
except ValueError:
    p = 0.5

range_x = lattice_x/2
range_y = lattice_y/2
end_point_id = lattice_x * lattice_y

size = 50*np.exp(-lattice_x/100)

num_repeat = 0

x_black = []
y_black = []
x_green = []
y_green = []
x_red = []
y_red = []

# Building of initial configuration

initialConfig = ff.initialConfig(lattice_x, lattice_y, p)
currentConfig = ff.initialFire(lattice_y, initialConfig)
fireCount = ff.fireCount(end_point_id, currentConfig)

# Stepwise fire spreading

while fireCount > 0:
        num_repeat+=1
        pointsCoordinates = ff.pointsCoordinates(end_point_id, currentConfig)
        x_black.append(pointsCoordinates[0])
        y_black.append(pointsCoordinates[1])
        x_green.append(pointsCoordinates[2])
        y_green.append(pointsCoordinates[3])
        x_red.append(pointsCoordinates[4])
        y_red.append(pointsCoordinates[5])
        fireCount = ff.fireCount(end_point_id, currentConfig)
        updatedConfig = ff.fireSpread(lattice_x, lattice_y, end_point_id, currentConfig)
        currentConfig = updatedConfig

#  Animation of forest fire

fig_title = "Forest Fire ($p$ = {0}, Lattice: {1} x {2})".format(p, lattice_x, lattice_y)

ax1 = fig.add_subplot(111, title=fig_title, xlabel='$X$', ylabel='$Y$',
        xlim=[-range_x, range_x], ylim=[-range_y , range_y])
ax1.set_xticks(np.linspace(-range_x, range_x, 5))
ax1.set_yticks(np.linspace(-range_y, range_y, 5))
#ax1.grid(b=True, which='major', color='#999999', linestyle='-')

configration_black = amp.blocks.Scatter(x_black, y_black, ax=ax1, s=size, color='black')
configration_green = amp.blocks.Scatter(x_green, y_green, ax=ax1, s=size, color='green')
configration_red = amp.blocks.Scatter(x_red, y_red, ax=ax1, s=size, color='red')

t = np.linspace(0, num_repeat-1, num_repeat)
timeline = amp.Timeline(t, units='steps', fps=30)

anim = amp.Animation([configration_black, configration_green, configration_red], timeline)
anim.controls()

savefile = "./gif/forest_fire_p{0}_{1}x{2}.png".format(p,lattice_x,lattice_y)

anim.save_gif(savefile)

plt.show()