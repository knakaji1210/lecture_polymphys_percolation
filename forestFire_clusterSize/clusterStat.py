# calculate cluster statistics

import numpy as np
from math import *
import matplotlib.pyplot as plt

def clusterStat(clusters_list, end_point_id, p):

    num_sites = []      # corresponds to s for s-cluster
    num_clusters = []   # corresponds to n_s for s-cluster

    total_num_clusters = len(clusters_list)
    num_clusters_max = np.max(clusters_list)
    num_clusters_min = np.min(clusters_list)
    total_num_occupied_sites = np.sum(clusters_list)
    # num_clusters_mean = np.mean(clusters_list)

    for i in range(end_point_id):
        num_clusters_i = [j for j in clusters_list if j == i]
        if not num_clusters_i == []:
            num_sites.append(i)
            total_num_clusters_i = len(num_clusters_i)
            num_clusters.append(total_num_clusters_i)

    ns_s = [x * y for (x, y) in zip(num_clusters, num_sites)]   # corresponds to n_s * s
    p_calc = np.sum(ns_s) / end_point_id
    cluster_size_mean1 = np.sum(ns_s) / np.sum(num_clusters)    # これはnum_clusters_meanと同じになる
    ws = ns_s / np.sum(ns_s)      # corresponds to w_s
    ws_s = [x * y for (x, y) in zip(ws, num_sites)]    # corresponds to w_s * s
    cluster_size_mean2 = np.sum(ws_s)
    cluster_size = cluster_size_mean2

    resultText0 = "$p$(set) = {}".format(p)
    resultText1 = "$p$(sim) = ${{{0:.3f}}}$".format(p_calc)
    resultText2 = "$n$(clusters) = {}".format(total_num_clusters)
    resultText3 = "$s$(max) = {}".format(num_clusters_max)
    resultText4 = "$s$(min) = {}".format(num_clusters_min)
    resultText5 = "$S$($n_{{ave}}$) = ${{{0:.1f}}}$".format(cluster_size_mean1)
    resultText6 = "$S$($w_{{ave}}$) = ${{{0:.1f}}}$".format(cluster_size_mean2)

    resultText =[resultText0, resultText1, resultText2, resultText3, resultText4, resultText5, resultText6]

    return num_sites, num_clusters, cluster_size, num_clusters_max, resultText
  