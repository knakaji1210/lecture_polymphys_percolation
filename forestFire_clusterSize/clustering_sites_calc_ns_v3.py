# Calculation of forest fire statistics (cluster size at fixed p)

# 250113コメント
# clustering_sites_calc_nspc_v2.pyからコピー
# nspcの計算だけでなくnsの計算ができるのだから名前もclustering_sites_calc_ns_v3.pyと変更
# それに伴う修正を加えた

import numpy as np
from math import *
import clusterFuncResult_rg as cfr
import clusterStat_v2 as cs
import clusterHist_v2 as ch
# 要チェック
import matplotlib.pyplot as plt
import time

try:
    lattice_x = int(input('X-Lattice Size (default=100): '))
except ValueError:
    lattice_x = 100

try:
    lattice_y = int(input('Y-Lattice Size (default=100): '))
except ValueError:
    lattice_y = 100

end_point_id = lattice_x * lattice_y

try:
    p = float(input('Probability (default=0.6): '))
except ValueError:
    p = 0.6

try:
    num_repeat = int(input('Number of Repetition (default=10): '))
except ValueError:
    num_repeat = 10

h_list = [lattice_x, lattice_y, p, num_repeat]

start_time = time.process_time()

clusters_list_rep = []

pc = 0.6

for i in range(num_repeat):
    clusters_list = cfr.buildClusterList(lattice_x, lattice_y, p)
    clusters_list.sort()
    if p >= pc:
        clusters_list = clusters_list[:-1] # percolation clusterを除外
    clusters_list_rep.append(clusters_list)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("i = {0}, elapsed time = {1:.1f} sec".format(i, elapsed_time))

hist_rep = []

for clusters_list in clusters_list_rep:
#    dataHist = ch.clusterHist(clusters_list, "wo", end_point_id) # num_repeatのところで抜いたのでここでは抜かなくていい
#    上の行（過去のコメント）で「抜かなくていい」と言っているのに"wo"となっているのはおかしい
    dataHist = ch.clusterHist(clusters_list, "w", end_point_id) # 250113に変更
    hist_rep.append(dataHist[1])

hist_x = dataHist[0]
hist_ave = np.mean(hist_rep, axis=0)
hist_std = np.std(hist_rep, axis=0)
bar_width = dataHist[2]

end_time = time.process_time()
elapsed_time = end_time - start_time

h_list.append(elapsed_time)

fig = plt.figure()

ax1 = fig.add_subplot(111, title="Distribution of $s$-clusters", xlabel='Cluster size, $s$', ylabel='Number of s-cluster, $n_{{s}}$($p$)')
ax1.set_xscale("log")
# ax1.bar(hist_x, hist_ave, width=bar_width, color='green')
ax1.bar(hist_x, hist_ave, width=bar_width, color='green', log=True)

ax1.errorbar(hist_x, hist_ave, yerr = hist_std, capsize=2, ecolor='red', fmt='none')

result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
result_text2 = "Repeat: {}".format(num_repeat)
result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)
result_text4 = "$p$ = {}".format(p)

fig.text(0.65, 0.8, result_text1)
fig.text(0.65, 0.75, result_text2)
fig.text(0.65, 0.70, result_text3)
fig.text(0.65, 0.65, result_text4)

savefile1 = "./data/h_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, p)
savefile2 = "./data/x_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, p)
savefile3 = "./data/y_mean_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, p)
savefile4 = "./data/y_std_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, p)
savefile5 = "./data/bw_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, p)

np.savetxt(savefile1, h_list)
np.savetxt(savefile2, hist_x)
np.savetxt(savefile3, hist_ave)
np.savetxt(savefile4, hist_std)
np.savetxt(savefile5, bar_width)

savefile = "./png/clusterSize_critical_{0}x{1}_p{2}.png".format(lattice_x,lattice_y, p)
fig.savefig(savefile, dpi=300)

plt.show()