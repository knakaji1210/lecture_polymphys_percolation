# 250323コメント
# sやnsをlogで処理する形に変更
# clustering_sites_calc_ns_v4.pyと連動
# v2まではnp.appendの引数の順番を間違えていた。下が正しい。
# ns_array = np.append(ns_array, ns)
# プログラム名をclustering_sites_ratio_ns_nspc_v3.pyに変更

import math
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def remove_inf(x_array, y_array):   # このバージョンでは利用していない
    f_inf_minus = -float('inf')

    x_list = []
    y_list = []

    for i in range(len(x_array)):
        if y_array[i] == f_inf_minus:
            pass
        else:
            x_list.append(x_array[i])
            y_list.append(y_array[i])

    new_x_array = np.array(x_list)
    new_y_array = np.array(y_list)

    return new_x_array, new_y_array

def remove_nan(x_array, y_array):

    x_list = []
    y_list = []

    for i in range(len(x_array)):
        if  math.isnan(y_array[i]) == True:
            pass
        else:
            x_list.append(x_array[i])
            y_list.append(y_array[i])

    new_x_array = np.array(x_list)
    new_y_array = np.array(y_list)

    return new_x_array, new_y_array

def expFit(x, a, b, c):
    return  a*np.exp(-c*x) + b

def polyFit(x, a, b):
    return  x**(1/a) + b

def fittedArray(x_array, param, func):
    if func == "exp":
        fitted_array = np.array([ expFit(x, param[0], param[1], param[2]) for x in x_array ])
    elif func == "poly":
        fitted_array = np.array([ polyFit(x, param[0], param[1]) for x in x_array ])
    return fitted_array

if __name__ == '__main__':
    try:
        lattice_x = int(input('X-Lattice Size (default=300): '))
    except ValueError:
        lattice_x = 300

    try:
        lattice_y = int(input('Y-Lattice y Size (default=300): '))
    except ValueError:
        lattice_y = 300

    '''
    Max probを0.6で行うと結果が思う形にならない。そこで0.59をベースにした。
    '''

    try:
        base_prob = float(input('Base probability (default=0.59): '))
    except ValueError:
        base_prob = 0.59

    lx = str(lattice_x)
    ly = str(lattice_y)
    pb = str(base_prob)

    log_s_file_pb = "./data/log_s_list_{0}x{1}_p{2}.txt".format(lx,ly,pb)
    log_ns_file_pb = "./data/log_ns_mean_list_{0}x{1}_p{2}.txt".format(lx,ly,pb)

    log_s_pb = np.loadtxt(log_s_file_pb, dtype=float)       # x軸のp=pbのlos(s)、他のpでも全て同じ
    log_ns_pb = np.loadtxt(log_ns_file_pb, dtype=float)

    orig_s_array = np.array([ int(10**log_s) for log_s in log_s_pb])
    len_s = orig_s_array.size

    try:
        max_prob = float(input('Max probability (default=0.58): '))
    except ValueError:
        max_prob = 0.58

    try:
        min_prob = float(input('Min probability (default=0.50): '))
    except ValueError:
        min_prob = 0.50

    num_prob = round((max_prob - min_prob)/0.01) + 1

    prob_array = np.linspace(min_prob, max_prob, num_prob)

    log_ns_array = np.array([])
    c_array = np.array([])
    cerr_array = np.array([])

    for prob in prob_array:
        p = "{:.2f}".format(prob)
        log_ns_file = "./data/log_ns_mean_list_{0}x{1}_p{2}.txt".format(lx,ly,p)
        log_ns = np.loadtxt(log_ns_file, dtype=float)
        log_ns_array = np.append(log_ns_array, log_ns)

    log_ns_array = log_ns_array.reshape(num_prob, len_s)   # np.appendすると1次元になるので整形

    fig_title1 = 'Ratio between the number of s-cluster, $n_{{s}}$($p$)/$n_{{s}}$($p_c$)'
    title1_x = '$s$'
    title1_y = 'log($n_{{s}}$($p$)/$n_{{s}}$($p_c$))'
    fig_title2 = 'Scaling of Cut-off'
    title2_x = '$p_{{c}}$ - $p$'
    title2_y = 'c'

    fig = plt.figure(figsize=(16.0, 8.0))
    ax1 = fig.add_subplot(121, title=fig_title1, xlabel=title1_x, ylabel=title1_y)
    ax1.set_xscale('log')
    ax2 = fig.add_subplot(122, title=fig_title2, xlabel=title2_x, ylabel=title2_y)

    n = 0

    for prob in prob_array:
        p = "{:.2f}".format(prob)
        ratio_array = log_ns_array[n] - log_ns_pb     # ns_arrayは既にlogになっているので比は引き算
        s_array = orig_s_array                        # 常にorig_s_arrayを参照する
        s_array, ratio_array = remove_nan(s_array, ratio_array)
        argm = np.argmax(ratio_array)
        param, cov = curve_fit(expFit, s_array[argm:], ratio_array[argm:], p0=[1,0,0.001], maxfev=8000)
        paramErr = np.sqrt(cov[2][2])
#        fit_s_array = np.linspace(s_array[0], s_array[-1], 100)    # 線形軸用
#        fit_func_ns = fittedArray(fit_s_array, param, "exp")       # 線形軸用
        fit_log_s_array = np.logspace(np.log10(s_array[0]), np.log10(s_array[-1]), 100)
        fit_func_ns = fittedArray(fit_log_s_array, param, "exp")
        ax1.scatter(s_array, ratio_array, label="p = {0}".format(p))
#        ax1.plot(fit_s_array, fit_func_ns)                         # 線形軸用
        ax1.plot(fit_log_s_array, fit_func_ns)
        c_array = np.append(c_array, param[2])
        cerr_array = np.append(cerr_array, paramErr)
        n += 1

    ax1.legend()

    pc = 0.6
    del_p_array = pc - prob_array
    param, cov = curve_fit(polyFit, del_p_array, c_array, sigma=cerr_array)
    paramErr = np.sqrt(cov[0][0])
    del_p = np.linspace(del_p_array[0], del_p_array[-1], 100)
    fit_func_c = fittedArray(del_p, param, "poly")
    ax2.scatter(del_p_array, c_array)
    ax2.errorbar(del_p_array, c_array, yerr = cerr_array, capsize=2, fmt='none')
    ax2.plot(del_p, fit_func_c)

    result_text1 = "$c$ ∝ ($p_{{c}}$ - $p$)$^{{1/\u03C3}}$"
    result_text2 = "\u03C3 = {0:.3f}±{1:.3f}".format(param[0], paramErr)
    fig.text(0.6, 0.8, result_text1)
    fig.text(0.6, 0.75, result_text2)

    savefile = "./png/clusterSize_ratio_ns_nspc_{0}x{1}.png".format(lattice_x,lattice_y)
    fig.savefig(savefile, dpi=300)

    plt.show()
