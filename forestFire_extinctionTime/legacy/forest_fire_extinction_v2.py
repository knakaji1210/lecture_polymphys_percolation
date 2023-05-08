# Calculation of forest fire extinction time

import numpy as np
from math import *
import forestFuncResult_v2 as ffr
import matplotlib.pyplot as plt
import animatplot as amp
from matplotlib import animation

fig = plt.figure()

lattice_x = 100     #500
lattice_y = 100     #300

p_min = 0.4
p_max = 0.8
p_step = 21         #21

p_list = np.linspace(p_min, p_max, p_step)
fireExtTime_mean_list = []

num_repeat = 50     #50

for p in p_list:

    fireExtTime_list = []

    for i in range(num_repeat):
        fireExtTime = ffr.fireExtinctionTime(lattice_x, lattice_y, p)
        fireExtTime_list.append(fireExtTime)

    fireExtTime_mean = np.mean(fireExtTime_list)
    
    print(fireExtTime_mean)
    fireExtTime_mean_list.append(fireExtTime_mean)

LongestTime = np.max(fireExtTime_mean_list)

ax = fig.add_subplot(111, title='Fire Extinction Time vs Probability of Green', 
            xlabel='Probability of Green', ylabel='Extinction Time',
            xlim=[p_min, p_max], ylim=[0, LongestTime*1.05])
ax.grid(b=True, which='major', color='#666666', linestyle='--')

ax.scatter(p_list, fireExtTime_mean_list)

np.savetxt("./data/p_list.txt", p_list)
np.savetxt("./data/fireExtTime_mean_list.txt", fireExtTime_mean_list)

#p_step_list, fireExtTime_step_list = ffr.drawStepEvolutionFunc(p_step, p_list, fireExtTime_mean_list)

#extinction_time = amp.blocks.Line(p_step_list, fireExtTime_step_list, ax=ax)

#timeline = amp.Timeline(p_list, fps=30)

#anim = amp.Animation([extinction_time], timeline)
#anim.controls()
#anim.save_gif("./gif/extinction_time")

fig.savefig("./png/forestFire_extinctionTime.png", dpi=300)

plt.show()