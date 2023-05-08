# Modeling of forest fire

import numpy as np
from math import *
import forestFunc as ff
import matplotlib.pyplot as plt
import animatplot as amp
from matplotlib import animation

fig = plt.figure()

lattice_x = 50
lattice_y = 25
range_x = lattice_x/2
range_y = lattice_y/2
end_point_id = lattice_x * lattice_y

p = 0.85

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

ax1 = fig.add_subplot(111, title='Forest Fire', xlabel='X', ylabel='Y',
        xlim=[-range_x, range_x], ylim=[-range_y , range_y])
ax1.set_xticks(np.linspace(-range_x, range_x, 5))
ax1.set_yticks(np.linspace(-range_y, range_y, 5))
#ax1.grid(b=True, which='major', color='#999999', linestyle='-')

configration_black = amp.blocks.Scatter(x_black, y_black, ax=ax1, color='black')
configration_green = amp.blocks.Scatter(x_green, y_green, ax=ax1, color='green')
configration_red = amp.blocks.Scatter(x_red, y_red, ax=ax1, color='red')

t = np.linspace(0, num_repeat-1, num_repeat)
timeline = amp.Timeline(t, units='steps', fps=30)

anim = amp.Animation([configration_black, configration_green, configration_red], timeline)
anim.controls()
anim.save_gif("./gif/forest_fire")

plt.show()