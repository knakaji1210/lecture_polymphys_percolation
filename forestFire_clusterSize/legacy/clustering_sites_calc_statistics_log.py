# Calculation of forest fire extinction time

import numpy as np
from math import *
import clusterFuncResult_rg as cfr
import clusterStat as cs
import matplotlib.pyplot as plt
import time

start = time.time()

lattice_x = 50     #500
lattice_y = 50     #300
end_point_id = lattice_x * lattice_y

p_min = 0.4
p_max = 0.8
p_step = 20         #21

#p_list = np.linspace(p_min, p_max, p_step)
p_list = np.logspace(np.log10(p_min), np.log10(p_max), p_step, base=10)
cluster_size_mean_list = []
cluster_size_std_list = []

num_repeat = 10     #50

#clusters_list = cfr.buildClusterList(lattice_x, lattice_y, p)
#print(clusters_list)

for p in p_list:

    cluster_size_list = []

    for i in range(num_repeat):
        clusters_list = cfr.buildClusterList(lattice_x, lattice_y, p)
        num_sites, num_clusters, cluster_size, resultText = cs.clusterStat(clusters_list, end_point_id, p)
        print(cluster_size)
        cluster_size_list.append(cluster_size)
    cluster_size_mean = np.mean(cluster_size_list)
    cluster_size_std = np.std(cluster_size_list)
    print(cluster_size_mean, cluster_size_std)
    cluster_size_mean_list.append(cluster_size_mean)
    cluster_size_std_list.append(cluster_size_std)

    elapsed_time = time.time() - start
    print(f"elapsed time: {elapsed_time:6f} sec")

print(cluster_size_mean_list)
print(cluster_size_std_list)


fig = plt.figure()

LargestSize = np.max(cluster_size_mean_list)

ax = fig.add_subplot(111, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Cluster Size',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-10, LargestSize*1.05])
ax.grid(b=True, which='major', color='#666666', linestyle='--')

ax.errorbar(p_list, cluster_size_mean_list, yerr = cluster_size_std_list, capsize=5)
ax.scatter(p_list, cluster_size_mean_list)

np.savetxt("./data/p_list.txt", p_list)
np.savetxt("./data/cluster_size_mean_list.txt", cluster_size_mean_list)
np.savetxt("./data/cluster_size_std_list.txt", cluster_size_std_list)

fig.savefig("./png/cluster_size_mean.png", dpi=300)

plt.show()