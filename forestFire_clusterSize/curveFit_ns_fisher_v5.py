# curve fitting for Fisher exponent

# 250113コメント
# curveFit_critical_nspc_v3.pyからコピー
# nspcの計算だけでなくnsの計算ができるのだから名前もcurveFit_critical_ns_v4.pyと変更
# それに伴う修正を加えた

# 上記コメントにさらにコメント（250321）
# そもそもFisher指数なので、これはp=pc=0.6について行うべきもの
# ただしns(p)/ns(pc)についての計算もpcについて行うと変になる（percolation clusterが抜ける分exp(-cs)とならない）ので
# ns(p=0.59)などの計算もできるようにしておくべきか

# 250314コメント
# sやnsをlogで処理する形に変更
# clustering_sites_calc_ns_v4.py、clusterHist_v3.pyと連動
# curve_fitのsigmaを使って重み付きフィッティングもできるようにした

# 250323コメント
# プログラム名をcurveFit_ns_fisher_v5.pyに変更

import math
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# header read

def head_read(lx,ly,p,choice):

    pc = 0.6
    prob = "{:.2f}".format(p)

    if p >= pc:
        if choice == "w":
            header_file = "./data/h_list_{0}x{1}_p{2}_w.txt".format(lx,ly,prob)
        elif choice == "wo":
            header_file = "./data/h_list_{0}x{1}_p{2}_wo.txt".format(lx,ly,prob)
    else:
        header_file = "./data/h_list_{0}x{1}_p{2}.txt".format(lx,ly,prob)

    h_list =[]

    f=open(header_file, 'r')
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

def file_read(lx,ly,p,choice):

    pc = 0.6
    prob = "{:.2f}".format(p)

    if p >= pc:
        if choice == "w":
            input1_file = "./data/log_s_list_{0}x{1}_p{2}_w.txt".format(lx,ly,prob)
            input2_file = "./data/log_ns_mean_list_{0}x{1}_p{2}_w.txt".format(lx,ly,prob)
            input3_file = "./data/log_ns_std_list_{0}x{1}_p{2}_w.txt".format(lx,ly,prob)
            input4_file = "./data/bw_list_{0}x{1}_p{2}_w.txt".format(lx,ly,prob)
        elif choice == "wo":
            input1_file = "./data/log_s_list_{0}x{1}_p{2}_wo.txt".format(lx,ly,prob)
            input2_file = "./data/log_ns_mean_list_{0}x{1}_p{2}_wo.txt".format(lx,ly,prob)
            input3_file = "./data/log_ns_std_list_{0}x{1}_p{2}_wo.txt".format(lx,ly,prob)
            input4_file = "./data/bw_list_{0}x{1}_p{2}_wo.txt".format(lx,ly,prob)
    else:
        input1_file = "./data/log_s_list_{0}x{1}_p{2}.txt".format(lx,ly,prob)
        input2_file = "./data/log_ns_mean_list_{0}x{1}_p{2}.txt".format(lx,ly,prob)
        input3_file = "./data/log_ns_std_list_{0}x{1}_p{2}.txt".format(lx,ly,prob)
        input4_file = "./data/bw_list_{0}x{1}_p{2}.txt".format(lx,ly,prob)

    x_array = np.array(file_open(input1_file))
    y_array = np.array(file_open(input2_file))
    yerr_array = np.array(file_open(input3_file))
    bw_array = np.array(file_open(input4_file))
    dataset = [ x_array, y_array, yerr_array, bw_array ]

    return dataset

# remove unwanted components

'''
250323コメント・・・以下は過去のコメント
要素として0を含むリストをlog10すると
RuntimeWarning: divide by zero
が出て、値が-infになる。それを除去するための関数がremove_inf
250314コメントとの連動で、読み込まれる
log_s_list、log_ns_mean_list
が既にlogされており、
log_ns_mean_list
には-infが含まれている。また
log_ns_std_list
にはnanが含まれている。
しかし、log_ns_mean_listで-infになっているところがnanになっているので
同じインデックスの要素をぬけば良いという発想で抜いている
250323コメント・・・ここから新しいコメント
計算順序変更のため、log_ns_mean_listやlog_ns_std_listにはもはや-infは含まれていない
一方、nanは含まれており、それを除去するための関数がremove_nan
同様にcurve_fitのsigmaに0が含まれているとエラーになるのでremove_zerosも追加
'''

def remove_infs(dataset):
    f_inf_minus = -float('inf')

    x_list = []
    y_list = []
    yerr_list = []

    for i in range(len(dataset[1])):
        if dataset[1][i] == f_inf_minus:
            pass
        else:
            x_list.append(dataset[0][i])
            y_list.append(dataset[1][i])
            yerr_list.append(dataset[2][i])

    x_array = np.array(x_list)
    y_array = np.array(y_list)
    yerr_array = np.array(yerr_list)
    new_dataset = [x_array, y_array, yerr_array]

    return new_dataset

def remove_nans(dataset):

    x_list = []
    y_list = []
    yerr_list = []

    for i in range(len(dataset[1])):
        if  math.isnan(dataset[1][i]) == True:
            pass
        else:
            x_list.append(dataset[0][i])
            y_list.append(dataset[1][i])
            yerr_list.append(dataset[2][i])

    x_array = np.array(x_list)
    y_array = np.array(y_list)
    yerr_array = np.array(yerr_list)
    new_dataset = [x_array, y_array, yerr_array]

    return new_dataset

def remove_zeros(dataset):

    x_list = []
    y_list = []
    yerr_list = []

    for i in range(len(dataset[2])):
        if  dataset[2][i] == 0:
            pass
        else:
            x_list.append(dataset[0][i])
            y_list.append(dataset[1][i])
            yerr_list.append(dataset[2][i])

    x_array = np.array(x_list)
    y_array = np.array(y_list)
    yerr_array = np.array(yerr_list)
    new_dataset = [x_array, y_array, yerr_array]

    return new_dataset

# curve fitting

def linearFit(x, a, b):     # 既にlogしたデータを読み込むので線形フィットで良い
    return  a*x + b

def fittedArray(x_array, param):
    fitted_array = np.array([ linearFit(x, param[0], param[1]) for x in x_array ])
    return fitted_array


if __name__ == '__main__':
    
    try:
        lattice_x = int(input('X-Lattice Size (default=200): '))
    except ValueError:
        lattice_x = 200

    try:
        lattice_y = int(input('Y-Lattice Size (default=100): '))
    except ValueError:
        lattice_y = 100

    try:
        p = float(input('Probability (default=0.6): '))
    except ValueError:
        p = 0.6

    lx = str(lattice_x)
    ly = str(lattice_y)

    pc = 0.6
    choice = "wo"

    if p >= pc:
        try:
            choice = input('with/without percolation cluster? (w or wo): ')
        except:
            choice = "wo"

    h_array = head_read(lx,ly,p,choice)
    num_repeat = int(h_array[3])
    elapsed_time = h_array[4]

    dataset = file_read(lx,ly,p,choice)

    logHist_x = dataset[0]
    logHist_y = dataset[1]
    logHist_y_std = dataset[2]
    bar_width = dataset[3]

    dataLogHist = [logHist_x, logHist_y, logHist_y_std] 
#    dataLogHist = remove_infs(dataLogHist) # -infが要素にないので不要になった
    dataLogHist = remove_nans(dataLogHist)
    dataLogHist = remove_zeros(dataLogHist)

#    param, cov = curve_fit(linearFit, dataLogHist[0], dataLogHist[1])
    param, cov = curve_fit(linearFit, dataLogHist[0], dataLogHist[1], sigma=dataLogHist[2]) # 重み付きフィッティング
    paramErr = np.sqrt(cov[0][0])

    print('fitting parameter: {}'.format(param))

    logHist_y_fit = fittedArray(dataLogHist[0], param)

    fig = plt.figure(figsize=(16.0, 8.0))

    ax1 = fig.add_subplot(121, title="Distribution of $s$-clusters", xlabel='Cluster size, Log($s$)', ylabel='Number of s-cluster, Log($n_{{s}}$($p$))')
    ax1.bar(logHist_x, logHist_y, width=bar_width, color='green')
    ax1.errorbar(logHist_x, logHist_y, yerr = logHist_y_std, capsize=2, ecolor='red', fmt='none')

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
    ax2.errorbar(dataLogHist[0], dataLogHist[1], yerr = dataLogHist[2], capsize=2, ecolor=u'#1f77b4', fmt='none')
    ax2.plot(dataLogHist[0], logHist_y_fit,  c='blue')
  
    result_text5 = "$n_{{s}}$($p$) ∝ $s$$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(param[0], paramErr)
    fig.text(0.75, 0.8, result_text5)

    prob = "{:.2f}".format(p)

    if p >= pc:
        if choice == "w":
            savefile = "./png/clusterSize_ns_{0}x{1}_p{2}_w_fitted.png".format(lattice_x,lattice_y, prob)
        elif choice == "wo":
            savefile = "./png/clusterSize_ns_{0}x{1}_p{2}_wo_fitted.png".format(lattice_x,lattice_y, prob)
    else:
        savefile = "./png/clusterSize_ns_{0}x{1}_p{2}_fitted.png".format(lattice_x,lattice_y, prob)

    fig.savefig(savefile, dpi=300)
    
    plt.show()