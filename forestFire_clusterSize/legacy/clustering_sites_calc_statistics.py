# Calculation of forest fire statistics (cluster size)

import numpy as np
from math import *
import clusterFuncResult_rg as cfr
import clusterStat as cs
import matplotlib.pyplot as plt
import time

start = time.time()

lattice_x = 100     #500
lattice_y = 100     #300
end_point_id = lattice_x * lattice_y

p_min = 0.4
p_max = 0.8
p_step = 11         #21

p_list = np.linspace(p_min, p_max, p_step)
cluster_size_mean_list = []
cluster_size_std_list = []
percolated_cluster_size_mean_list = [] # added
percolated_cluster_size_std_list = [] # added

num_repeat = 3     #50

#clusters_list = cfr.buildClusterList(lattice_x, lattice_y, p)
#print(clusters_list)

for p in p_list:

    cluster_size_list = []
    percolated_clusters_size_list = [] # added

    for i in range(num_repeat):
        clusters_list = cfr.buildClusterList(lattice_x, lattice_y, p)
        num_sites, num_clusters, cluster_size, num_clusters_max, resultText = cs.clusterStat(clusters_list, end_point_id, p) # modified
        print(cluster_size)
        cluster_size_list.append(cluster_size)
        percolated_clusters_size_list.append(num_clusters_max) # added
    cluster_size_mean = np.mean(cluster_size_list)
    cluster_size_std = np.std(cluster_size_list)
    print(cluster_size_mean, cluster_size_std)
    cluster_size_mean_list.append(cluster_size_mean)
    cluster_size_std_list.append(cluster_size_std)
    percolated_cluster_size_mean = np.mean(percolated_clusters_size_list) # added
    percolated_cluster_size_std = np.std(percolated_clusters_size_list) # added
    percolated_cluster_size_mean_list.append(percolated_cluster_size_mean) # added
    percolated_cluster_size_std_list.append(percolated_cluster_size_std) # added

    elapsed_time = time.time() - start
    print(f"elapsed time: {elapsed_time:6f} sec")

print(cluster_size_mean_list)
print(cluster_size_std_list)


fig = plt.figure(figsize=(12,5))

LargestSize = np.max(cluster_size_mean_list)
LargestSize2 = np.max(percolated_cluster_size_mean_list)

ax1 = fig.add_subplot(121, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Cluster Size',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-10, LargestSize*1.05])
ax1.grid(b=True, which='major', color='#666666', linestyle='--')

ax1.errorbar(p_list, cluster_size_mean_list, yerr = cluster_size_std_list, capsize=5)
ax1.scatter(p_list, cluster_size_mean_list)

ax2 = fig.add_subplot(122, title='Mean Percolation Cluster Size vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Percolation Cluster Size',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-10, LargestSize2*1.05])
ax2.grid(b=True, which='major', color='#666666', linestyle='--')

ax2.errorbar(p_list, percolated_cluster_size_mean_list, yerr = percolated_cluster_size_std_list, capsize=5)
ax2.scatter(p_list, percolated_cluster_size_mean_list)

np.savetxt("./data/p_list.txt", p_list)
np.savetxt("./data/cluster_size_mean_list.txt", cluster_size_mean_list)
np.savetxt("./data/cluster_size_std_list.txt", cluster_size_std_list)
np.savetxt("./data/percolated_cluster_size_mean_list.txt", percolated_cluster_size_mean_list) # added
np.savetxt("./data/percolated_cluster_size_std_list.txt", percolated_cluster_size_std_list) # added

fig.savefig("./png/cluster_size_mean.png", dpi=300)

plt.show()