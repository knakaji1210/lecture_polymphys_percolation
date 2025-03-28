# Calculation of forest fire statistics (cluster size at fixed p =< pc)

# 250314コメント
# sやnsをlogで処理する形に変更
# clusterHist_v3.pyと連動

# 250322コメント
# clusterHist_v3.pyでlog_histに含まれてしまう-infをnanに変換済み
# hist_ave = np.mean(hist_rep, axis=0)
# ではnanが含まれているとnp.meanがnanになってしまう。そこでnp.nanmeanを使う。
# hist_ave = np.nanmean(hist_rep, axis=0)

# 250323コメント
# プログラム名をclustering_sites_ns_v4.pyに変更

import numpy as np
from math import *
import clusterFuncResult_rg as cfr
import clusterHist_v3 as ch
import matplotlib.pyplot as plt
import time

try:
    lattice_x = int(input('X-Lattice Size (default=200): '))
except ValueError:
    lattice_x = 200

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
    num_repeat = int(input('Number of Repetition (default=100): '))
except ValueError:
    num_repeat = 100

pc = 0.6
choice = "wo"

if p >= pc:
    try:
        choice = input('with/without percolation cluster? (w or wo): ')
    except:
        choice = "wo"

h_list = [ lattice_x, lattice_y, p, num_repeat ]    # ヘッダ情報

start_time = time.process_time()

clusters_list_rep = []

pc = 0.6

for i in range(num_repeat):
    clusters_list = cfr.buildClusterList(lattice_x, lattice_y, p)
    clusters_list.sort()
    if p >= pc:
        if choice == "w":
            pass
        elif choice == "wo":
            clusters_list = clusters_list[:-1] # percolation clusterを除外
    log_clusters_list = [ np.log10(s) for s in clusters_list ]  # 250320に追加
    clusters_list_rep.append(log_clusters_list)
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("i = {0}, elapsed time = {1:.1f} sec".format(i, elapsed_time))

hist_rep = []

for clusters_list in clusters_list_rep:
    dataHist = ch.clusterHist(clusters_list, end_point_id) # 250113に変更
    hist_rep.append(dataHist[1])

hist_log_s = dataHist[0]
hist_log_ns_ave = np.nanmean(hist_rep, axis=0)
hist_log_ns_std = np.nanstd(hist_rep, axis=0)
bar_width = dataHist[2]
max_range = dataHist[3]

end_time = time.process_time()
elapsed_time = end_time - start_time

h_list.append(elapsed_time)

fig = plt.figure()

ax1 = fig.add_subplot(111, title="Distribution of $s$-clusters", 
                      xlabel='Cluster size, Log($s$)', ylabel='Number of s-cluster, Log($n_{{s}}$($p$))',
                      xlim=(0,max_range))
ax1.bar(hist_log_s, hist_log_ns_ave, width=bar_width, color='green')
ax1.errorbar(hist_log_s, hist_log_ns_ave, yerr = hist_log_ns_std, capsize=2, ecolor='red', fmt='none')

result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
result_text2 = "Repeat: {}".format(num_repeat)
result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)
result_text4 = "$p$ = {}".format(p)

fig.text(0.65, 0.8, result_text1)
fig.text(0.65, 0.75, result_text2)
fig.text(0.65, 0.70, result_text3)
fig.text(0.65, 0.65, result_text4)

prob = "{:.2f}".format(p)

if p >= pc:
    if choice == "w":
        savefile1 = "./data/h_list_{0}x{1}_p{2}_w.txt".format(lattice_x,lattice_y, prob)
        savefile2 = "./data/log_s_list_{0}x{1}_p{2}_w.txt".format(lattice_x,lattice_y, prob)
        savefile3 = "./data/log_ns_mean_list_{0}x{1}_p{2}_w.txt".format(lattice_x,lattice_y, prob)
        savefile4 = "./data/log_ns_std_list_{0}x{1}_p{2}_w.txt".format(lattice_x,lattice_y, prob)
        savefile5 = "./data/bw_list_{0}x{1}_p{2}_w.txt".format(lattice_x,lattice_y, prob)
    elif choice == "wo":
        savefile1 = "./data/h_list_{0}x{1}_p{2}_wo.txt".format(lattice_x,lattice_y, prob)
        savefile2 = "./data/log_s_list_{0}x{1}_p{2}_wo.txt".format(lattice_x,lattice_y, prob)
        savefile3 = "./data/log_ns_mean_list_{0}x{1}_p{2}_wo.txt".format(lattice_x,lattice_y, prob)
        savefile4 = "./data/log_ns_std_list_{0}x{1}_p{2}_wo.txt".format(lattice_x,lattice_y, prob)
        savefile5 = "./data/bw_list_{0}x{1}_p{2}_wo.txt".format(lattice_x,lattice_y, prob)
else:
    savefile1 = "./data/h_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, prob)
    savefile2 = "./data/log_s_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, prob)
    savefile3 = "./data/log_ns_mean_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, prob)
    savefile4 = "./data/log_ns_std_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, prob)
    savefile5 = "./data/bw_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y, prob)

np.savetxt(savefile1, h_list)
np.savetxt(savefile2, hist_log_s)
np.savetxt(savefile3, hist_log_ns_ave)
np.savetxt(savefile4, hist_log_ns_std)
np.savetxt(savefile5, bar_width)

if p >= pc:
    if choice == "w":
        savefile = "./png/clusterSize_ns_{0}x{1}_p{2}_w.png".format(lattice_x,lattice_y, prob)
    elif choice == "wo":
        savefile = "./png/clusterSize_ns_{0}x{1}_p{2}_wo.png".format(lattice_x,lattice_y, prob)
else:
    savefile = "./png/clusterSize_ns_{0}x{1}_p{2}.png".format(lattice_x,lattice_y, prob)

fig.savefig(savefile, dpi=300)

plt.show()