# Calculation of forest fire statistics (cluster structure)

import numpy as np
from math import *
import buildClusterStructure_v2 as bcs
import clusterStruct_v2 as cs
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

end_point_id = lattice_x * lattice_y

p_list = np.linspace(p_min, p_max, p_step)
cluster_size_mean_list = []
cluster_size_std_list = []
corr_len_mean_list = []
corr_len_std_list = []

try:
    num_repeat = int(input('Number of Repetition (default=10): '))
except ValueError:
    num_repeat = 10

h_list = [lattice_x, lattice_y, p_min, p_max, p_step, num_repeat]

start_time = time.process_time()

for p in p_list:

    cluster_size_list = []
    corr_len_list = []
    for i in range(num_repeat):
        cluster_attribute_list = bcs.buildClusterStructure(lattice_x, lattice_y, p)
        num_sites, num_clusters, cluster_size, corr_len, resultText = cs.clusterStruct(cluster_attribute_list, end_point_id, p)
#        print(cluster_size)
#        print(corr_len)
        cluster_size_list.append(cluster_size)
        corr_len_list.append(corr_len)
    cluster_size_mean = np.mean(cluster_size_list)
    cluster_size_std = np.std(cluster_size_list)
    corr_len_mean = np.mean(corr_len_list)
    corr_len_std = np.std(corr_len_list)
#    print(cluster_size_mean, cluster_size_std)
#    print(corr_len_mean, corr_len_std)
    cluster_size_mean_list.append(cluster_size_mean)
    cluster_size_std_list.append(cluster_size_std)
    corr_len_mean_list.append(corr_len_mean)
    corr_len_std_list.append(corr_len_std)

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("p = {0:.2f}, elapsed time = {1:.1f} sec".format(p, elapsed_time))

h_list.append(elapsed_time)

print(cluster_size_mean_list)
print(cluster_size_std_list)
print(corr_len_mean_list)
print(corr_len_std_list)

fig = plt.figure(figsize=(12, 5))

LargestSize = np.max(cluster_size_mean_list)
LargestLength = np.max(corr_len_mean_list)

ax1 = fig.add_subplot(121, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='$p$', ylabel='$S$',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-LargestSize*0.05, LargestSize*1.05])
ax1.grid(b=True, which='major', color='#666666', linestyle='--')

ax1.errorbar(p_list, cluster_size_mean_list, yerr = cluster_size_std_list, capsize=5)
ax1.scatter(p_list, cluster_size_mean_list)

ax2 = fig.add_subplot(122, title='Mean Correlation Length vs Probability of Occupying Sites', 
            xlabel='$p$', ylabel='$ξ$',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-1, LargestLength*1.05])
ax2.grid(b=True, which='major', color='#666666', linestyle='--')

ax2.errorbar(p_list, corr_len_mean_list, yerr = corr_len_std_list, capsize=5)
ax2.scatter(p_list, corr_len_mean_list)

result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
result_text2 = "Repeat: {}".format(num_repeat)
result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)

fig.text(0.15, 0.8, result_text1)
fig.text(0.15, 0.75, result_text2)
fig.text(0.15, 0.70, result_text3)

savefile1 = "./data/h_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile2 = "./data/p_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile3 = "./data/S_mean_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile4 = "./data/S_std_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile5 = "./data/xi_mean_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile6 = "./data/xi_std_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)

np.savetxt(savefile1, h_list)
np.savetxt(savefile2, p_list)
np.savetxt(savefile3, cluster_size_mean_list)
np.savetxt(savefile4, cluster_size_std_list)
np.savetxt(savefile5, corr_len_mean_list)
np.savetxt(savefile6, corr_len_std_list)

savefile = "./png/clusterStructure_{0}x{1}_p{2}-{3}.png".format(lattice_x,lattice_y, p_min, p_max)
fig.savefig(savefile, dpi=300)

plt.show()