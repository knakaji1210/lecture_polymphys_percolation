import numpy as np
import matplotlib.pyplot as plt

def clusterHist(clusters_list, choice, div):

    if choice == "w":
        pass
    elif choice == "wo":
        clusters_list = clusters_list[:-1] # percolation clusterを除外する場合

    min_cluster = np.min(clusters_list)
    max_cluster = np.max(clusters_list)

    hist, bins = np.histogram(clusters_list, bins=np.logspace(np.log10(min_cluster), np.log10(max_cluster), div))

    hist_x = []
    for i in range(1, len(bins)):
        hist_x.append(np.sqrt(bins[i-1]*bins[i]))

    bar_width = [i*0.1 for i in hist_x]

    log_hist = [ np.log10(x) for x in hist ]
    log_hist_x = [ np.log10(x) for x in hist_x ]

    dataHist = [hist_x, hist, bar_width, log_hist_x, log_hist, ]

    return dataHist