# calculate cluster statistics

import numpy as np
from math import *
import matplotlib.pyplot as plt

def clusterStruct(cluster_attribute_list, end_point_id, p):

    clusters_list = [cluster_attribute_list[i][0] for i in range(len(cluster_attribute_list))]
    radius_gyration_list = [cluster_attribute_list[i][1] for i in range(len(cluster_attribute_list))]
#    print(clusters_list)
#    print(radius_gyration_list)

    num_sites = []      # corresponds to s for s-cluster
    num_clusters = []   # corresponds to n_s for s-cluster
    rog_mean = []   # corresponds to Sqrt(<Rs^2>) for s-cluster

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

    slice_num = 0

    for j in num_clusters:
        radius_gyration = radius_gyration_list[slice_num:slice_num + j]
        radius_gyration_mean = np.mean(radius_gyration)
        rog_mean.append(radius_gyration_mean)
        slice_num+= j

    #print(num_sites)
    #print(num_clusters)
    #print(rog_mean)

    ns_s = [x * y for (x, y) in zip(num_clusters, num_sites)]   # corresponds to n_s * s
    p_calc = np.sum(ns_s) / end_point_id
    cluster_size_mean1 = np.sum(ns_s) / np.sum(num_clusters)    # これはnum_clusters_meanと同じになる
    ws = ns_s / np.sum(ns_s)      # corresponds to w_s
    ws_s = [x * y for (x, y) in zip(ws, num_sites)]    # corresponds to w_s * s
    cluster_size_mean2 = np.sum(ws_s)
    cluster_size = cluster_size_mean2

    sq_rog_mean = [x * y for (x, y) in zip(rog_mean, rog_mean)]
    sq_rog_mean_w = [x * y for (x, y) in zip(ws_s, sq_rog_mean)]
    sq_corr_len = 2*np.sum(sq_rog_mean_w) / cluster_size_mean2
    corr_len = np.sqrt(sq_corr_len)

    resultText0 = "p(set) = "+str(p)
    resultText1 = "p(sim) = "+str(round(p_calc,3))
    resultText2 = "n(clusters) = "+str(total_num_clusters)
    resultText3 = "s(max) = "+str(num_clusters_max)
    resultText4 = "s(min) = "+str(num_clusters_min)
    resultText5 = "S1_ave = "+str(round(cluster_size_mean1,1))
    resultText6 = "S2_ave = "+str(round(cluster_size_mean2,1))
    resultText7 = "xi = "+str(round(corr_len,1))

    resultText =[resultText0, resultText1, resultText2, resultText3, resultText4, resultText5, resultText6]

    return num_sites, num_clusters, cluster_size, corr_len, resultText