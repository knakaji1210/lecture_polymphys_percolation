# 250323コメント
# このバージョンには致命的なミスがある（v3のコメント参照）。
# そういうわけでこれはlegacyに移動。

import math
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

'''
要素として0を含むリストをlog10すると
RuntimeWarning: divide by zero
が出て、値が-infになる。それを除去するための関数がremove_inf

要素として含まれるnanを除去するための関数がremove_nan

これらはnumpyのもっと良い関数で記述できないか検討が必要
（一旦リストに戻したりしちゃっているので・・・）
'''

def remove_inf(x_array, y_array):
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

def linearFit(x, a, b):
    return  a*x + b

def polyFit(x, a, b):
    return  x**(1/a) + b

if __name__ == '__main__':
    try:
        ls_x = int(input('X-Lattice Size (default=200): '))
    except ValueError:
        ls_x = 200

    try:
        ls_y = int(input('Y-Lattice y Size (default=100): '))
    except ValueError:
        ls_y = 100

    '''
    Max probを0.6で行うと結果が思う形にならない。そこで0.59をベースにした。
    '''

    try:
        px = float(input('Maximim probability (default=0.59): '))
    except ValueError:
        px = 0.59

    lattice_x = str(ls_x)
    lattice_y = str(ls_y)
    max_prob = str(px)

    max_prob_s_file = "./data/x_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y,max_prob)
    max_prob_ns_file = "./data/y_mean_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y,max_prob)

    max_prob_s = np.loadtxt(max_prob_s_file, dtype=float)
    max_prob_ns = np.loadtxt(max_prob_ns_file, dtype=float)

    len_s = max_prob_s.size                         # 基本的に入力されるファイルの要素数は皆同じはず
    log_s = [ np.log10(s) for s in max_prob_s ]

    try:
        num_p = int(input('Number of other probabilities (default=10): '))
    except ValueError:
        num_p = 10

    ns_array = np.array([])
    p_array = np.array([])
    c_array = np.array([])

    for n in range(num_p):
        try:
            p = float(input('Probabilities (default=0.58): '))
        except ValueError:
            p = 0.58
        prob = str(p)
        ns_file = "./data/y_mean_list_{0}x{1}_p{2}.txt".format(lattice_x,lattice_y,prob)
        ns = np.loadtxt(ns_file, dtype=float)
        ns_array = np.append(ns, ns_array)
        p_array = np.append(p, p_array)
    
    ns_array = ns_array.reshape(num_p, len_s)   # np.appendすると1次元になるので整形

    fig_title1 = 'Ratio between the number of s-cluster, $n_{{s}}$($p$)/$n_{{s}}$($p=p_c$)'
    fig_title2 = 'Scaling of Cut-off'
    title_y = 'log($n_{{s}}$($p$)/$n_{{s}}$($p=p_c$))'

    fig = plt.figure(figsize=(16.0, 8.0))
    ax1 = fig.add_subplot(121, title=fig_title1, xlabel='$s$', ylabel=title_y)
    ax2 = fig.add_subplot(122, title=fig_title2, xlabel='$p_{{c}}$ - $p$', ylabel='c')

    for n in range(num_p):
        ratio_nsp = ns_array[n]/max_prob_ns
        log_ratio = np.log(ratio_nsp)
        updated_s_array, updated_log_ratio = remove_inf(max_prob_s, log_ratio)
        updated_s_array, updated_log_ratio = remove_nan(updated_s_array, updated_log_ratio)
        argm = np.argmax(updated_log_ratio)
        param, cov = curve_fit(linearFit, updated_s_array[argm:], updated_log_ratio[argm:])
        paramErr = np.sqrt(cov[0][0])
        fit_func = [ param[0]*s + param[1] for s in updated_s_array ]
        ax1.scatter(updated_s_array, updated_log_ratio)
        ax1.plot(updated_s_array, fit_func, c='black')
        c_array = np.append(param[0], c_array)
    
    pc = 0.6
    delp_array = pc - p_array
    param, cov = curve_fit(polyFit, delp_array, c_array)
    paramErr = np.sqrt(cov[0][0])
    delp = np.linspace(np.min(delp_array), np.max(delp_array), 100)
    fit_func2 = [ x**(1/param[0]) + param[1] for x in delp ]
    ax2.scatter(delp_array, c_array)
    ax2.plot(delp, fit_func2)
    print(param[0])
    print(paramErr)

    result_text1 = "$c$ ∝ ($p_{{c}}$ - $p$)$^{{1/\u03C3}}$"
    result_text2 = "\u03C3 = {0:.3f}±{1:.3f}".format(param[0], paramErr)
    fig.text(0.6, 0.8, result_text1)
    fig.text(0.6, 0.75, result_text2)

    savefile = "./png/clusterSize_ratio_ns_nspc_{0}x{1}_p{2}.png".format(lattice_x,lattice_y, p)
    fig.savefig(savefile, dpi=300)

    plt.show()
