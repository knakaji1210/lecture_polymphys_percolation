import numpy as np
from math import *
import matplotlib.pyplot as plt

clusters_list = [1, 1, 257, 2, 3, 1, 44, 1, 1, 9, 28, 7, 90, 1, 1, 1, 20, 1, 1, 1, 1, 4, 1, 1, 3, 46, 1, 2, 1, 1, 7, 1, 1, 41, 1, 9, 1, 2, 44, 1, 1, 5, 19, 1, 1, 2, 5, 1, 1, 5, 2, 1, 30, 8, 81, 16, 1, 1, 1, 106, 239, 4, 7, 1, 4, 9, 3, 1, 2, 1, 4, 1, 4, 2, 1, 1, 1, 2, 2, 40, 8, 1, 4, 1, 1, 7, 2, 1, 1, 1, 34, 3, 1, 1, 2, 1, 1, 6, 28, 2, 19, 6, 6, 1, 1, 2, 7, 1, 1, 1, 4, 2, 1, 1, 1, 1, 1]

total_num_sites = 2500
p_set = 0.58

num_sites = []      # corresponds to s for s-cluster
num_clusters = []   # corresponds to n_s for s-cluster

total_num_clusters = len(clusters_list)
num_clusters_max = np.max(clusters_list)
num_clusters_min = np.min(clusters_list)
total_num_occupied_sites = np.sum(clusters_list)
# num_clusters_mean = np.mean(clusters_list)

for i in range(total_num_sites):
    num_clusters_i = [j for j in clusters_list if j == i]
    if not num_clusters_i == []:
        num_sites.append(i)
        total_num_clusters_i = len(num_clusters_i)
        num_clusters.append(total_num_clusters_i)

ns_s = [x * y for (x, y) in zip(num_clusters, num_sites)]   # corresponds to n_s * s
p_calc = np.sum(ns_s) / total_num_sites
cluster_size_mean1 = np.sum(ns_s) / np.sum(num_clusters)    # これはnum_clusters_meanと同じになる
ws = ns_s / np.sum(ns_s)      # corresponds to w_s
ws_s = [x * y for (x, y) in zip(ws, num_sites)]    # corresponds to w_s * s
cluster_size_mean2 = np.sum(ws_s)

resultText1 = "n(clusters) = "+str(total_num_clusters)
resultText2 = "s(max) = "+str(num_clusters_max)
resultText3 = "s(min) = "+str(num_clusters_min)
resultText4 = "p(set) = "+str(p_set)
resultText5 = "p(sim) = "+str(round(p_calc,3))
resultText6 = "S1 = "+str(round(cluster_size_mean1,1))
resultText7 = "S2 = "+str(round(cluster_size_mean2,1))


fig = plt.figure()

plt.bar(num_sites, num_clusters, width=2, log=True)

fig.text(0.70, 0.80, resultText1)
fig.text(0.70, 0.75, resultText2)
fig.text(0.70, 0.70, resultText3)
fig.text(0.70, 0.65, resultText4)
fig.text(0.70, 0.60, resultText5)
fig.text(0.70, 0.55, resultText6)
fig.text(0.70, 0.50, resultText7)

plt.show()