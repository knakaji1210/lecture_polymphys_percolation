# Calculation of forest fire extinction time

import numpy as np
from math import *
import forestFuncResult_v2 as ffr
import matplotlib.pyplot as plt
import time


try:
    lattice_x = int(input('X-Lattice Size (default=100): '))
except ValueError:
    lattice_x = 100

try:
    lattice_y = int(input('Y-Lattice Size (default=100): '))
except ValueError:
    lattice_y = 100

try:
    p_min = float(input('Minimum Probability (default=0.4): '))
except ValueError:
    p_min = 0.4

try:
    p_max = float(input('Maximum Probability (default=0.8): '))
except ValueError:
    p_max = 0.8

try:
    p_step = int(input('Number of Probabilities (default=21): '))
except ValueError:
    p_step = 21

p_list = np.linspace(p_min, p_max, p_step)
fireExtTime_mean_list = []

try:
    num_repeat = int(input('Number of Repetition (default=50): '))
except ValueError:
    num_repeat = 50

h_list = [lattice_x, lattice_y, p_min, p_max, p_step, num_repeat]

start_time = time.process_time()

for p in p_list:

    fireExtTime_list = []

    for i in range(num_repeat):
        fireExtTime = ffr.fireExtinctionTime(lattice_x, lattice_y, p)
        fireExtTime_list.append(fireExtTime)

    fireExtTime_mean = np.mean(fireExtTime_list)

    fireExtTime_mean_txt = 't_ext = {0:.1f} (p = {1:.2f})'.format(fireExtTime_mean, p)
    
    print(fireExtTime_mean_txt)
    fireExtTime_mean_list.append(fireExtTime_mean)

LongestTime = np.max(fireExtTime_mean_list)

end_time = time.process_time()
elapsed_time = end_time - start_time

h_list.append(elapsed_time)

fig = plt.figure()

fig_title = "Fire Extinction Time vs Probability of Green"

ax = fig.add_subplot(111, title=fig_title, 
            xlabel='$p$', ylabel='$t_{{Extinction}}$')
#            xlim=[p_min, p_max], ylim=[0, LongestTime*1.05])
ax.grid(visible=True, which='major', color='#666666', linestyle='--')

ax.scatter(p_list, fireExtTime_mean_list)

result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
result_text2 = "Repeat: {}".format(num_repeat)
result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)

fig.text(0.6, 0.8, result_text1)
fig.text(0.6, 0.75, result_text2)
fig.text(0.6, 0.70, result_text3)

savefile1 = "./data/h_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile2 = "./data/p_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile3 = "./data/t_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile4 = "./png/forestFire_extinctionTime_{0}x{1}_p{2}-{3}.png".format(lattice_x,lattice_y, p_min, p_max)

np.savetxt(savefile1, h_list)
np.savetxt(savefile2, p_list)
np.savetxt(savefile3, fireExtTime_mean_list)
fig.savefig(savefile4, dpi=300)

plt.show()