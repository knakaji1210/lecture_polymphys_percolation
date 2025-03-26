# calculate cluster statistics

# p > pcのときにpercolation clusterを除外しないで統計を取っていたため、以下の不具合があった
# p = P + sigma(ns*s)が満たされない
# S(w_ave)がpercolation clusterを含んだ計算になっていた
# 以上の修正を行なった（250115）

# 250325コメント
# 後日忘れないように色々コメントを追加

import numpy as np
from math import *
import matplotlib.pyplot as plt

'''
clusters_list
clusterFuncResult_rg.pyのbuildClusterList関数で得られるsのリスト
例えば
[1, 2, 5, 5, 25, 6, 2, 1, 1, 1, 26, 1, 5, 1, 1, 1, 46, 54, 1, 13, 1, 1, 1, 1, 1, 5, 1, 1, 1, 2, 10, 1, 1, 2, 70, 53, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 5, 3, 1, 1, 1, 5, 3, 1, 2, 12, 2, 1, 9, 1, 1, 1, 1, 3, 3, 12, 10, 1, 2, 1, 1]
のようなリスト。これを整形して、num_sitesはどんなsがあるかのみ抽出、例えば
num_sites =  [1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13, 25, 26, 46, 53, 54, 70]
さらにnum_clustersはそれぞれのsに対して何個のクラスターがあるかを数える。例えば
num_clusters =  [44, 7, 4, 2, 6, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1]
これは例えばs=1のクラスターが44個、s=2のクラスターが7個、s=3のクラスターが4個、という意味。
'''

def clusterStat(clusters_list, end_point_id, p):

    num_sites = []      # corresponds to s for s-cluster
    num_clusters = []   # corresponds to n_s for s-cluster

    total_num_clusters = len(clusters_list)             # 存在する全クラスターの総数（percolation cluster除外前）
    num_clusters_max = np.max(clusters_list)            # これは最大のクラスターサイズ、上の例では70（percolation cluster除外前）
    num_clusters_min = np.min(clusters_list)            # 最小のクラスターサイズ、上の例では1（percolation cluster除外前）
    total_num_occupied_sites = np.sum(clusters_list)    # 全てのクラスターの総サイト数、つまり占有サイトの総数（percolation cluster除外前）
    # num_clusters_mean = np.mean(clusters_list)

    # ここから追加（250115)
    pc = 0.6
    clusters_list.sort()    # clusters_listは順番がバラバラなのでソート
    if p >= pc:
        clusters_list = clusters_list[:-1] # percolation clusterを除外
    # ここまで（これによってp >= pcのとき、clusters_listの中にpercolation clusterは存在しない）

    for i in range(end_point_id):   # clusters_listをnum_sitesとnum_clustersに整理する手続き
        num_clusters_i = [j for j in clusters_list if j == i]
        if not num_clusters_i == []:
            num_sites.append(i)
            total_num_clusters_i = len(num_clusters_i)
            num_clusters.append(total_num_clusters_i)

    ns_s = [x * y for (x, y) in zip(num_clusters, num_sites)]   # corresponds to n_s * s
    # p_calc = np.sum(ns_s) / end_point_id                      # 過去のでpercolation clusterを抜いて計算してしまうので利用しない
    p_calc = total_num_occupied_sites / end_point_id            # 新たに追加（むしろ素直な定義）
    n_ave_cluster_size = np.sum(ns_s) / np.sum(num_clusters)  # corresponds to S(n_ave)、num_clusters_meanと同じになる
    ws = ns_s / np.sum(ns_s)                                    # corresponds to w_s
    ws_s = [x * y for (x, y) in zip(ws, num_sites)]             # corresponds to w_s * s
    w_ave_cluster_size = np.sum(ws_s)                           # corresponds to S(w_ave) (p < pcのみ意味がある) 

# ここはlog_Pを計算するためにlog10(0)を発生させないためにもっと簡単に記述する。
#    if p >= pc:
#        p_cluster_prob = num_clusters_max / end_point_id        # corresponds to P
#    else:
#        p_cluster_prob = 0                                      # p < pcのときはPを定義しない

    p_cluster_prob = num_clusters_max / end_point_id            # corresponds to P (p > pcのみ意味がある)

    resultText0 = "$p$(set) = {}".format(p)
    resultText1 = "$p$(sim) = ${{{0:.3f}}}$".format(p_calc)
    resultText2 = "$n$(clusters) = {}".format(total_num_clusters)
    resultText3 = "$s$(max) = {}".format(num_clusters_max)
    resultText4 = "$s$(min) = {}".format(num_clusters_min)
    resultText5 = "$S$($n_{{ave}}$) = ${{{0:.1f}}}$".format(n_ave_cluster_size)
    resultText6 = "$S$($w_{{ave}}$) = ${{{0:.1f}}}$".format(w_ave_cluster_size)
    resultText7 = "$P$ = ${{{0:.2f}}}$".format(p_cluster_prob)

    resultText =[ resultText0, resultText1, resultText2, resultText3, resultText4, resultText5, resultText6, resultText7 ]

    return num_sites, num_clusters, w_ave_cluster_size, p_cluster_prob, resultText
  