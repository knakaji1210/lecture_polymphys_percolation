# Modeling of forest fire

import numpy as np
import random as rd
from math import *
import matplotlib.pyplot as plt
import forestFunc as pf
import animatplot as amp
from matplotlib import animation

fig = plt.figure()

lattice_x = 50
lattice_y = 25
range_x = lattice_x/2
range_y = lattice_y/2
end_point_id = lattice_x * lattice_y
#probe_point_id = int(lattice_x*lattice_y/4 + lattice_y/2)

pc = 0.2

num_repert = 10
#num_sample = 5
#num_status_mean = num_repert - num_sample

x_black = []
y_black = []
x_green = []
y_green = []
x_red = []
y_red = []

probe_point_status = []
probe_point_status_mean = []
num_step = []

# Building of initial configuration

initialConfig = pf.initialConfig(lattice_x, lattice_y, pc)
currentConfig = pf.initialFire(lattice_x, lattice_y, initialConfig)

# Stepwise point exchange & Status check of probe point 

for i in range(num_repert):
#        probe_point = currentConfig[probe_point_id]
#        probe_point_status.append(probe_point[1])
        pointsCoordinates = pf.pointsCoordinates(end_point_id, currentConfig)
        x_black.append(pointsCoordinates[0])
        y_black.append(pointsCoordinates[1])
        x_green.append(pointsCoordinates[2])
        y_green.append(pointsCoordinates[3])
        x_red.append(pointsCoordinates[4])
        y_red.append(pointsCoordinates[5])
        updatedConfig = pf.exchangePairs(lattice_x, lattice_y, end_point_id, currentConfig)
        currentConfig = updatedConfig

#  Stepwise evolution of statistics of probe point status

#for i in range(num_repert):
#    probe_point_status_extracted = []
#    if i > num_status_mean:
#        pass
#    else:
#        for j in range(num_sample):
#            probe_point_status_extracted.append(probe_point_status[i+j])
#    num_step.append(i)
#    probe_point_status_mean.append(np.mean(probe_point_status_extracted))

#  Animation of statistics of probe point status

ax1 = fig.add_subplot(111, title='Forest Fire', xlabel='X', ylabel='Y',
        xlim=[-range_x, range_x], ylim=[-range_y , range_y])
#ax1.set_xticks(np.linspace(-range_x, range_x, lattice_x + 1))
#ax1.set_yticks(np.linspace(-range_y, range_y, lattice_y + 1))
ax1.set_xticks(np.linspace(-range_x, range_x, 5))
ax1.set_yticks(np.linspace(-range_y, range_y, 5))
#ax1.grid(b=True, which='major', color='#999999', linestyle='-')

configration_black = amp.blocks.Scatter(x_black, y_black, ax=ax1, color='black')
configration_green = amp.blocks.Scatter(x_green, y_green, ax=ax1, color='green')
configration_red = amp.blocks.Scatter(x_red, y_red, ax=ax1, color='red')

step, probe_point_mean = pf.drawStepEvolutionFunc(num_repert, num_step, probe_point_status_mean)

t = np.linspace(0, num_repert-1, num_repert)
timeline = amp.Timeline(t, units='steps', fps=30)

anim = amp.Animation([configration_black, configration_green, configration_red], timeline)
anim.controls()
anim.save_gif("./gif/forest_fire")

plt.show()