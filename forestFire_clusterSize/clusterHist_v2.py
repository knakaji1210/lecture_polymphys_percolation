import numpy as np

def clusterHist(clusters_list, choice, maxSize):

    if choice == "w":
        pass
    elif choice == "wo":
        clusters_list = clusters_list[:-1] # percolation clusterを除外する場合

    min_cluster = np.min(clusters_list) # not used
    max_cluster = np.max(clusters_list) # not used

    hist_div = int(np.log10(maxSize)*5)

#   hist, bins = np.histogram(clusters_list, bins=np.logspace(np.log10(min_cluster), np.log10(max_cluster), div))
    hist, bins = np.histogram(clusters_list, bins=np.logspace(0, np.log10(maxSize), hist_div))  # took simpler way on 20230109

    hist_x = []
    for i in range(1, len(bins)):
        hist_x.append(np.sqrt(bins[i-1]*bins[i]))

    bar_width = [0.2*i for i in hist_x]

    dataHist = [ hist_x, hist, bar_width ]

    return dataHist