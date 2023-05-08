# Modeling of forest fire

import numpy as np
from math import *
import clusterFunc_rg as crg
import clusterStat as cs
import matplotlib.pyplot as plt
import animatplot as amp
from matplotlib import animation

fig = plt.figure(figsize=(16.0, 8.0))

lattice_x = 20
lattice_y = 20
range_x = lattice_x/2
range_y = lattice_y/2
end_point_id = lattice_x * lattice_y

p = 0.62

x_black = []
y_black = []
x_green = []
y_green = []
x_red = []
y_red = []

# Building of initial configuration

initialConfig = crg.initialConfig(lattice_x, lattice_y, p)
greenCount = crg.greenCount(end_point_id, initialConfig)

# Setting a firing point

num_steps = 0
#num_repeat = 10
clusters_list = []

while greenCount > 0:
        fireCount = 0
        while fireCount == 0:
                currentConfig = crg.initialFire(end_point_id, initialConfig)
                fireCount = crg.fireCount(end_point_id, currentConfig)
                

# Stepwise fire spreading
        num_occupied_sites = 0
        while fireCount > 0:
                num_steps+=1
                pointsCoordinates = crg.pointsCoordinates(end_point_id, currentConfig)
                x_black.append(pointsCoordinates[0])
                y_black.append(pointsCoordinates[1])
                x_green.append(pointsCoordinates[2])
                y_green.append(pointsCoordinates[3])
                x_red.append(pointsCoordinates[4])
                y_red.append(pointsCoordinates[5])
                fireCount = crg.fireCount(end_point_id, currentConfig)
                greenCount = crg.greenCount(end_point_id, currentConfig)
#                print(greenCount)
                num_occupied_sites += fireCount
                updatedConfig = crg.fireSpread(lattice_x, lattice_y, end_point_id, currentConfig)
                currentConfig = updatedConfig
        clusters_list.append(num_occupied_sites)

# print(clusters_list)

num_sites, num_clusters, cluster_size, num_clusters_max, resultText = cs.clusterStat(clusters_list, end_point_id, p)

print(num_sites)
print(num_clusters)

#  Animation of forest fire

ax1 = fig.add_subplot(121, title='Forest Fire', xlabel='X', ylabel='Y',
        xlim=[-range_x, range_x], ylim=[-range_y , range_y])
ax1.set_xticks(np.linspace(-range_x, range_x, 5))
ax1.set_yticks(np.linspace(-range_y, range_y, 5))
#ax1.grid(b=True, which='major', color='#999999', linestyle='-')

configration_black = amp.blocks.Scatter(x_black, y_black, ax=ax1, s=15, color='black')
configration_green = amp.blocks.Scatter(x_green, y_green, ax=ax1, s=15, color='green')
configration_red = amp.blocks.Scatter(x_red, y_red, ax=ax1, s=15, color='red')

bar_width = [i*0.3 for i in num_sites]

ax2 = fig.add_subplot(122, title="Distribution of s-clusters", xlabel='Cluster size, s', ylabel='Number of s-cluster')
ax2.set_xscale("log")
ax2.bar(num_sites, num_clusters, width=bar_width, color='green', log=True)
#ax2.scatter(num_sites, num_clusters, color='green')

for i in range(len(resultText)):
        fig.text(0.80, 0.80 - 0.05*i, resultText[i])

t = np.linspace(0, num_steps-1, num_steps)
timeline = amp.Timeline(t, units='steps', fps=30)

anim = amp.Animation([configration_black, configration_green, configration_red], timeline)
anim.controls()
anim.save_gif("./gif/forest_fire_regular_firing")

plt.show()