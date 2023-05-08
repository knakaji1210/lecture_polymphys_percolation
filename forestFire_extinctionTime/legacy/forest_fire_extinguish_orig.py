# Calculation of forest fire extinction time

import numpy as np
from math import *
import forestFuncResult as ffr
import matplotlib.pyplot as plt
import animatplot as amp
from matplotlib import animation

fig = plt.figure()

lattice_x = 50
lattice_y = 25

p_min = 0.6
p_max = 1
p_step = 21

p_list = np.linspace(p_min, p_max, p_step)
fireExtTime_mean_list = []

num_repeat = 30

for p in p_list:

    fireExtTime_list = []

    for i in range(num_repeat):
        fireExtTime = ffr.fireExtinctionTime(lattice_x, lattice_y, p)
        fireExtTime_list.append(fireExtTime)

    fireExtTime_mean = np.mean(fireExtTime_list)
    
    print(fireExtTime_mean)
    fireExtTime_mean_list.append(fireExtTime_mean)

ax = fig.add_subplot(111, title='Fire Extinction Time vs Probability of Green', 
            xlabel='Probability of Green', ylabel='Extinction Time',
            xlim=[p_min, p_max], ylim=[0, 100])
ax.grid(b=True, which='major', color='#666666', linestyle='--')

#ax.scatter(p_list, fireExtTime_mean_list)

p_step_list, fireExtTime_step_list = ffr.drawStepEvolutionFunc(p_step, p_list, fireExtTime_mean_list)

extinction_time = amp.blocks.Line(p_step_list, fireExtTime_step_list, ax=ax)

#t = np.linspace(0, p_step-1, p_step)
#timeline = amp.Timeline(t, units='steps', fps=30)

timeline = amp.Timeline(p_list, fps=30)

anim = amp.Animation([extinction_time], timeline)
#anim.controls()
anim.save_gif("./gif/extinction_time")

plt.show()