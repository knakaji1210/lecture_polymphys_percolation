# Modeling of forest fire (random firing)

import numpy as np
from math import *
import clusterFunc_rd as crd
import matplotlib.pyplot as plt
import animatplot as amp

fig = plt.figure(figsize=(10.0, 8.0))

lattice_x = 100
lattice_y = 60
range_x = lattice_x/2
range_y = lattice_y/2
end_point_id = lattice_x * lattice_y

p = 0.55

x_black = []
y_black = []
x_green = []
y_green = []
x_red = []
y_red = []

# Building of initial configuration

initialConfig = crd.initialConfig(lattice_x, lattice_y, p)

# Setting a firing point

num_steps = 0
num_repeat = 10
cluster_list = []

for num in range(num_repeat):
        fireCount = 0
        while fireCount == 0:
                currentConfig = crd.initialFire(end_point_id, initialConfig)
                fireCount = crd.fireCount(end_point_id, currentConfig)
                

# Stepwise fire spreading
        num_cluster = 0
        while fireCount > 0:
                num_steps+=1
                pointsCoordinates = crd.pointsCoordinates(end_point_id, currentConfig)
                x_black.append(pointsCoordinates[0])
                y_black.append(pointsCoordinates[1])
                x_green.append(pointsCoordinates[2])
                y_green.append(pointsCoordinates[3])
                x_red.append(pointsCoordinates[4])
                y_red.append(pointsCoordinates[5])
                fireCount = crd.fireCount(end_point_id, currentConfig)
                num_cluster += fireCount
                updatedConfig = crd.fireSpread(lattice_x, lattice_y, end_point_id, currentConfig)
                currentConfig = updatedConfig
        cluster_list.append(num_cluster)

# numpyのバージョンアップにより、""ndarray from ragged nested sequences"の制限が厳しくなり、
# animatplotの途中でエラーが出るようになった。そのための修正が以下の６行
x_black = np.asanyarray(x_black, dtype=object)
y_black = np.asanyarray(y_black, dtype=object)
x_green = np.asanyarray(x_green, dtype=object)
y_green = np.asanyarray(y_green, dtype=object)
x_red = np.asanyarray(x_red, dtype=object)
y_red = np.asanyarray(y_red, dtype=object)

# print(cluster_list)

#  Animation of forest fire

ax1 = fig.add_subplot(111, title='Forest Fire', xlabel='X', ylabel='Y',
        xlim=[-range_x, range_x], ylim=[-range_y , range_y])
ax1.set_xticks(np.linspace(-range_x, range_x, 5))
ax1.set_yticks(np.linspace(-range_y, range_y, 5))
#ax1.grid(b=True, which='major', color='#999999', linestyle='-')

configration_black = amp.blocks.Scatter(x_black, y_black, ax=ax1, s=20, color='black')
configration_green = amp.blocks.Scatter(x_green, y_green, ax=ax1, s=20, color='green')
configration_red = amp.blocks.Scatter(x_red, y_red, ax=ax1, s=20, color='red')

t = np.linspace(0, num_steps-1, num_steps)
timeline = amp.Timeline(t, units='steps', fps=30)

anim = amp.Animation([configration_black, configration_green, configration_red], timeline)
anim.controls()
anim.save_gif("./gif/forest_fire_random_firing")

plt.show()