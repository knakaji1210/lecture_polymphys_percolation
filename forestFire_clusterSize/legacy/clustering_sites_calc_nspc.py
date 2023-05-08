# Calculation of forest fire extinction time

import numpy as np
from math import *
import clusterFuncResult_rg as cfr
import clusterStat as cs
import clusterHist as ch
import matplotlib.pyplot as plt
import time

start = time.time()

lattice_x = 100     #500
lattice_y = 100     #300
end_point_id = lattice_x * lattice_y

pc = 0.6

num_repeat = 1     #50
clusters_list_rep = []

for i in range(num_repeat):
    clusters_list = cfr.buildClusterList(lattice_x, lattice_y, pc)
    clusters_list.sort()
    clusters_list = clusters_list[:-1]
    clusters_list_rep+= clusters_list

elapsed_time = time.time() - start

fig = plt.figure()

dataHist = ch.clusterHist(clusters_list, "wo", 15) # num_repeatのところで抜いたのでここでは抜かなくていい

ax1 = fig.add_subplot(111, title="Distribution of s-clusters", xlabel='Cluster size, s', ylabel='Number of s-cluster')
ax1.set_xscale("log")
ax1.bar(dataHist[0], dataHist[1], width=dataHist[2], color='green', log=True)

#ax2 = fig.add_subplot(122, title="Scaling of Log(n_s)", xlabel='Log(s)', ylabel='Log(n_s)')
#ax2.scatter(dataHist[3], dataHist[4])

resultText1 = "p = "+str(pc)
resultText2 = f"elapsed time: {elapsed_time:.1f} sec"
fig.text(0.6, 0.75, resultText1)
fig.text(0.6, 0.70, resultText2)

np.savetxt("./data/log_hist_x.txt", dataHist[3])
np.savetxt("./data/log_hist.txt", dataHist[4])

fig.savefig("./png/fisher_exponent.png", dpi=300)

plt.show()