# curve fitting for Fisher exponent

# 250113コメント
# curveFit_critical_nspc_v3.pyからコピー
# nspcの計算だけでなくnsの計算ができるのだから名前もcurveFit_critical_ns_v4.pyと変更
# それに伴う修正を加えた

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

'''
How to use
% python3 curveFit_critical_ns_v3.py args[1] args[2] args[3] args[4]  args[5]
args[1] ./data/h_list_100x100_p0.6.txt
args[2] ./data/x_list_100x100_p0.6.txt
args[3] ./data/y_mean_list_100x100_p0.6.txt
args[4] ./data/y_std_list_100x100_p0.6.txt 
args[5] ./data/bw_list_100x100_p0.6.txt 
'''
    
def head_read():

    h_list =[]

    input_file = args[1]

    f=open(input_file, 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        data = float(datalist[i].rstrip('\n'))
        h_list.append(data)
    f.close()

    h_array = np.array(h_list)

    return h_array

# file read

def file_open(input_file):
    x_list = []
    f=open(input_file, 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        data = float(datalist[i].rstrip('\n'))
        x_list.append(data)
    f.close()
    return x_list

def file_read():

    input1 = args[2]
    input2 = args[3]
    input3 = args[4]
    input4 = args[5]

    x_array = np.array(file_open(input1))
    y_array = np.array(file_open(input2))
    yerr_array = np.array(file_open(input3))
    bw_array = np.array(file_open(input4))
    dataset = [x_array, y_array, yerr_array, bw_array]

    return dataset

'''
要素として0を含むリストをlog10すると
RuntimeWarning: divide by zero
が出て、値が-infになる。それを除去するための関数
'''


def remove_inf(dataset):
    f_inf_minus = -float('inf')

    x_list = []
    y_list = []

    for i in range(len(dataset[1])):
        if dataset[1][i] == f_inf_minus:
            pass
        else:
            x_list.append(dataset[0][i])
            y_list.append(dataset[1][i])

    x_array = np.array(x_list)
    y_array = np.array(y_list)
    dataset = [x_array, y_array]

    return dataset

def loglogFit(x, a, b):
    return  a*x + b

def fittedArray(x_array, param):
    fitted_array = [loglogFit(num, param[0], param[1]) for num in x_array]
    return fitted_array


if __name__ == '__main__':
    args = sys.argv

    h_array = head_read()

    lattice_x = int(h_array[0])
    lattice_y = int(h_array[1])
    p = h_array[2]
    num_repeat = int(h_array[3])
    elapsed_time = h_array[4]

    dataset = file_read()

    hist_x = dataset[0]
    hist_ave = dataset[1]
    hist_std = dataset[2]
    bar_width = dataset[3]

    with np.errstate(divide='ignore'):
        logHist_x = [ np.log10(x) for x in hist_x ]
        logHist_y = [ np.log10(y) for y in hist_ave ]

    dataLogHist_orig = [logHist_x, logHist_y] 
    dataLogHist = remove_inf(dataLogHist_orig)

    param, cov = curve_fit(loglogFit, dataLogHist[0], dataLogHist[1])
    paramErr = np.sqrt(cov[0][0])

    print('fitting parameter: {}'.format(param))

    logHist_y_fit = fittedArray(dataLogHist[0], param)

    fig = plt.figure(figsize=(16.0, 8.0))

    ax1 = fig.add_subplot(121, title="Distribution of $s$-clusters", xlabel='Cluster size, $s$', ylabel='Number of s-cluster, $n_{{s}}$($p$)')
    ax1.set_xscale("log")
    # ax1.bar(hist_x, hist_ave, width=bar_width, color='green')
    ax1.bar(hist_x, hist_ave, width=bar_width, color='green', log=True)

    ax1.errorbar(hist_x, hist_ave, yerr = hist_std, capsize=2, ecolor='red', fmt='none')

    result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
    result_text2 = "Repeat: {}".format(num_repeat)
    result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)
    result_text4 = "$p$ = {}".format(p)

    fig.text(0.35, 0.8, result_text1)
    fig.text(0.35, 0.75, result_text2)
    fig.text(0.35, 0.70, result_text3)
    fig.text(0.35, 0.65, result_text4)

    ax2 = fig.add_subplot(122, title='Scaling of Number of $s$-cluster', 
            xlabel='Log($s$)', ylabel='Log($n_{{s}}$)')
    ax2.grid(visible=True, which='major', color='#666666', linestyle='--')

    ax2.scatter(dataLogHist[0], dataLogHist[1], marker='o', c=u'#1f77b4')
    ax2.plot(dataLogHist[0], logHist_y_fit,  c='blue')

#    resultText = "n_s (p) ∝ tau^("+str(round(param[0],3))+")"


    result_text5 = "$n_{{s}}$($p$) ∝ $s$$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(param[0], paramErr)
    fig.text(0.75, 0.8, result_text5)

    savefile = "./png/clusterSize_critical_fit_{0}x{1}_p{2}.png".format(lattice_x,lattice_y, p)
    fig.savefig(savefile, dpi=300)
    
    plt.show()