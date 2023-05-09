# Calculation of forest fire statistics (cluster structure)

import numpy as np
from math import *
import buildClusterStructure as bcs
import clusterStruct_v2 as cs
import matplotlib.pyplot as plt
import time

start = time.time()

lattice_x = 50     #500
lattice_y = 50     #300
end_point_id = lattice_x * lattice_y

p_min = 0.1
p_max = 0.9
p_step = 17         #21

p_list = np.linspace(p_min, p_max, p_step)
cluster_size_mean_list = []
cluster_size_std_list = []
corr_len_mean_list = []
corr_len_std_list = []

num_repeat = 10     #50

for p in p_list:

    cluster_size_list = []
    corr_len_list = []
    for i in range(num_repeat):
        cluster_attribute_list = bcs.buildClusterStructure(lattice_x, lattice_y, p)

        num_sites, num_clusters, cluster_size, corr_len, resultText = cs.clusterStruct(cluster_attribute_list, end_point_id, p)
        print(cluster_size)
        print(corr_len)
        cluster_size_list.append(cluster_size)
        corr_len_list.append(corr_len)
    cluster_size_mean = np.mean(cluster_size_list)
    cluster_size_std = np.std(cluster_size_list)
    corr_len_mean = np.mean(corr_len_list)
    corr_len_std = np.std(corr_len_list)
    print(cluster_size_mean, cluster_size_std)
    print(corr_len_mean, corr_len_std)
    cluster_size_mean_list.append(cluster_size_mean)
    cluster_size_std_list.append(cluster_size_std)
    corr_len_mean_list.append(corr_len_mean)
    corr_len_std_list.append(corr_len_std)

    elapsed_time = time.time() - start
    print(f"elapsed time: {elapsed_time:6f} sec")

print(cluster_size_mean_list)
print(cluster_size_std_list)
print(corr_len_mean_list)
print(corr_len_std_list)


fig = plt.figure(figsize=(12.0, 10.0))

LargestSize = np.max(cluster_size_mean_list)
LargestLength = np.max(corr_len_mean_list)

ax1 = fig.add_subplot(221, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Cluster Size',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-1, LargestSize*1.05])
ax1.grid(b=True, which='major', color='#666666', linestyle='--')

ax1.errorbar(p_list, cluster_size_mean_list, yerr = cluster_size_std_list, capsize=5)
ax1.scatter(p_list, cluster_size_mean_list)

ax2 = fig.add_subplot(222, title='Mean Correlation Length vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Correlation Length',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-1, LargestLength*1.05])
ax2.grid(b=True, which='major', color='#666666', linestyle='--')

ax2.errorbar(p_list, corr_len_mean_list, yerr = corr_len_std_list, capsize=5)
ax2.scatter(p_list, corr_len_mean_list)

log_cluster_size_mean_list = [ log10(x) for x in cluster_size_mean_list ]
log_cluster_size_std_list = [ log10(x) for x in cluster_size_std_list ]
log_corr_len_mean_list = [ log10(y) for y in corr_len_mean_list ]
log_corr_len_std_list = [ log10(y) for y in corr_len_std_list ]

ax3 = fig.add_subplot(223, title='Mean Correlation Length vs Mean Cluster Size', 
            xlabel='Log(Mean Cluster Size)', ylabel='Log(Mean Correlation Length)')
ax3.grid(b=True, which='major', color='#666666', linestyle='--')

#ax3.errorbar(log_cluster_size_mean_list, log_corr_len_mean_list, xerr = log_cluster_size_std_list, yerr = log_corr_len_std_list, capsize=5)
ax3.scatter(log_cluster_size_mean_list, log_corr_len_mean_list)

np.savetxt("./data/p_list.txt", p_list)
np.savetxt("./data/cluster_size_mean_list.txt", cluster_size_mean_list)
np.savetxt("./data/cluster_size_std_list.txt", cluster_size_std_list)
np.savetxt("./data/corr_len_mean_list.txt", corr_len_mean_list)
np.savetxt("./data/corr_len_std_list.txt", corr_len_std_list)

fig.savefig("./png/cluster_size_structure.png", dpi=300)

plt.show()