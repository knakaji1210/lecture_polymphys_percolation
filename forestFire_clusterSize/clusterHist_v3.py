# 250314コメント
# sやnsをlogで処理する形に変更
# clustering_sites_calc_ns_v4.pyと連動

# 250322コメント
# log_histには-infが含まれることがあり、それらをnanに変換（18行目）

import numpy as np

def clusterHist(clusters_list, maxSize):

    max_range = np.log10(maxSize*0.6)       # percolation clusterより大きいclusterはない

    hist, bins = np.histogram(clusters_list, bins=25, range=(0,max_range))  # 250320に変更

    with np.errstate(divide='ignore'):
        log_hist = [ np.log10(h) for h in hist ]
        log_hist = [ np.nan if x == -np.inf else x for x in log_hist ]

    hist_x = []
    bar_width = []

    for i in range(1, len(bins)):
        hist_x.append((bins[i-1]+bins[i])/2)
        bar_width.append(0.9*(bins[i]-bins[i-1]))

    dataHist = [ hist_x, log_hist, bar_width, max_range ]

    return dataHist