# Calculation of forest fire statistics (cluster structure)

# 250329コメント
# pを変えてSとxiの計算をしていくのだが、これは同時に行った方が良いので、中身は変更せず
# フィッティング範囲、描画範囲だけ変えれば良い。
# ただし、clusterStruct_v3を使っているのでSの方の振る舞いは以前から変化している
# （Pクラスターを除外した結果、p > p_cでSが減少していく）

# curveFit_critical_xi_v5.py
# との連動を考え、こちらでlogの配列も計算することにした。
# ただし、xi_meanをlogしたものと、log_xi_meanは異なるので注意。

import numpy as np
from math import *
import buildClusterStructure_v3 as bcs
import clusterStruct_v3 as cs
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

try:
    p_min = float(input('Minimum Probability (default=0.4): '))
except ValueError:
    p_min = 0.4

try:
    p_max = float(input('Maximum Probability (default=0.8): '))
except ValueError:
    p_max = 0.8

try:
    p_step = int(input('Number of Probabilities (default=21): '))
except ValueError:
    p_step = 21

try:
    num_repeat = int(input('Number of Repetition (default=10): '))
except ValueError:
    num_repeat = 10

end_point_id = lattice_x * lattice_y
h_list = [lattice_x, lattice_y, p_min, p_max, p_step, num_repeat]

p_list = np.linspace(p_min, p_max, p_step)
S_mean_list = []
S_std_list = []
xi_mean_list = []
xi_std_list = []
log_S_mean_list = []
log_S_std_list = []
log_xi_mean_list = []
log_xi_std_list = []

start_time = time.process_time()

'''
cs.clusterStructの返り値について
num_sites           ・・・sのリスト
num_clusters        ・・・nsのリスト
w_ave_cluster_size  ・・・S（weight-averaged mean cluster size）
xi                  ・・・xi（correlation length）
resultText          ・・・結果のテキスト
'''

for p in p_list:

    S_list = []      # num_repeat回のSを格納するリスト
    xi_list = []     # num_repeat回のxiを格納するリスト
    log_S_list = []  # num_repeat回のlog_Sを格納するリスト
    log_xi_list = [] # num_repeat回のlog_xiを格納するリスト

    for i in range(num_repeat):
        cluster_attribute_list = bcs.buildClusterStructure(lattice_x, lattice_y, p)
        num_sites, num_clusters, S, xi, resultText = cs.clusterStruct(cluster_attribute_list, end_point_id, p)
        S_list.append(S)    # Sはmean cluster size
        xi_list.append(xi)  # xiはcorrelation length
        log_S = np.log10(S)
        log_xi = np.log10(xi)
        log_S_list.append(log_S)
        log_xi_list.append(log_xi)

    S_mean = np.mean(S_list)        # num_repeat回のSの平均
    S_std = np.std(S_list)          # num_repeat回のSの標準偏差
    S_mean_list.append(S_mean)      # 異なるpに対するSの平均を格納するリスト
    S_std_list.append(S_std)        # 異なるpに対するSの標準偏差を格納するリスト

    xi_mean = np.mean(xi_list)      # num_repeat回のxiの平均
    xi_std = np.std(xi_list)        # num_repeat回のxiの標準偏差
    xi_mean_list.append(xi_mean)    # 異なるpに対するxiの平均を格納するリスト
    xi_std_list.append(xi_std)      # 異なるpに対するPの標準偏差を格納するリスト

    log_S_mean = np.mean(log_S_list)        # num_repeat回のlog_Sの平均
    log_S_std = np.std(log_S_list)          # num_repeat回のlog_Sの標準偏差
    log_S_mean_list.append(log_S_mean)      # 異なるpに対するlog_Sの平均を格納するリスト
    log_S_std_list.append(log_S_std)        # 異なるpに対するlog_Sの標準偏差を格納するリスト

    log_xi_mean = np.mean(log_xi_list)      # num_repeat回のlog_xiの平均
    log_xi_std = np.std(log_xi_list)        # num_repeat回のlog_xiの標準偏差
    log_xi_mean_list.append(log_xi_mean)    # 異なるpに対するlog_xiの平均を格納するリスト
    log_xi_std_list.append(log_xi_std)      # 異なるpに対するlog_xiの標準偏差を格納するリスト

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    print("p = {0:.2f}, elapsed time = {1:.1f} sec".format(p, elapsed_time))

h_list.append(elapsed_time)

fig = plt.figure(figsize=(12, 5))

S_max = np.max(S_mean_list)
xi_max = np.max(xi_mean_list)

ax1 = fig.add_subplot(121, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='$p$', ylabel='$S$',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-S_max*0.05, S_max*1.05])
ax1.grid(visible=True, which='major', color='#666666', linestyle='--')

ax1.errorbar(p_list, S_mean_list, yerr = S_std_list, capsize=5)
ax1.scatter(p_list, S_mean_list)

ax2 = fig.add_subplot(122, title='Correlation Length vs Probability of Occupying Sites', 
            xlabel='$p$', ylabel='$ξ$',
            xlim=[p_min*0.95, p_max*1.05], ylim=[-xi_max*0.05, xi_max*1.05])
ax2.grid(visible=True, which='major', color='#666666', linestyle='--')

ax2.errorbar(p_list, xi_mean_list, yerr = xi_std_list, capsize=5)
ax2.scatter(p_list, xi_mean_list)

result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
result_text2 = "Repeat: {}".format(num_repeat)
result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)

fig.text(0.15, 0.8, result_text1)
fig.text(0.15, 0.75, result_text2)
fig.text(0.15, 0.70, result_text3)

savefile1 = "./data/h_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile2 = "./data/p_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile3 = "./data/S_mean_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile4 = "./data/S_std_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile5 = "./data/xi_mean_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile6 = "./data/xi_std_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile7 = "./data/log_S_mean_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile8 = "./data/log_S_std_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile9 = "./data/log_xi_mean_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)
savefile10 = "./data/log_xi_std_list_{0}x{1}_p{2}-{3}.txt".format(lattice_x,lattice_y, p_min, p_max)

np.savetxt(savefile1, h_list)
np.savetxt(savefile2, p_list)
np.savetxt(savefile3, S_mean_list)
np.savetxt(savefile4, S_std_list)
np.savetxt(savefile5, xi_mean_list)
np.savetxt(savefile6, xi_std_list)
np.savetxt(savefile7, log_S_mean_list)
np.savetxt(savefile8, log_S_std_list)
np.savetxt(savefile9, log_xi_mean_list)
np.savetxt(savefile10, log_xi_std_list)

savefile = "./png/clusterStructure_{0}x{1}_p{2}-{3}.png".format(lattice_x,lattice_y, p_min, p_max)
fig.savefig(savefile, dpi=300)

plt.show()