# curve fitting for correlation length (p < pc)

# 250329コメント
# clustering_sites_cluster_structure_v4.py、clusterStruct_v3.pyと連動

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# header read

def head_read(lx,ly,p_min,p_max):

    header_file = "./data/h_list_{0}x{1}_p{2}-{3}.txt".format(lx,ly,p_min,p_max)

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

def file_read(lx,ly,p_min,p_max):

    input1_file = "./data/p_list_{0}x{1}_p{2}-{3}.txt".format(lx,ly,p_min,p_max)
    input2_file = "./data/xi_mean_list_{0}x{1}_p{2}-{3}.txt".format(lx,ly,p_min,p_max)
    input3_file = "./data/xi_std_list_{0}x{1}_p{2}-{3}.txt".format(lx,ly,p_min,p_max)
    input4_file = "./data/log_xi_mean_list_{0}x{1}_p{2}-{3}.txt".format(lx,ly,p_min,p_max)
    input5_file = "./data/log_xi_std_list_{0}x{1}_p{2}-{3}.txt".format(lx,ly,p_min,p_max)

    p_array = np.array(file_open(input1_file))
    xi_array = np.array(file_open(input2_file))
    xierr_array = np.array(file_open(input3_file))
    log_xi_array = np.array(file_open(input4_file))
    log_xierr_array = np.array(file_open(input5_file))
    dataset = [ p_array, xi_array, xierr_array, log_xi_array, log_xierr_array ]

    return dataset

def data_split(dataset, pc):    # p < pcのデータを抽出
    p_array = np.array([i for i in dataset[0] if round(i,2) < pc])
    xi_array = dataset[1][:len(p_array)]
    xierr_array = dataset[2][:len(p_array)]
    log_xi_array = dataset[3][:len(p_array)]
    log_xierr_array = dataset[4][:len(p_array)]
    split_dataset = [ p_array, xi_array, xierr_array, log_xi_array, log_xierr_array ]
    return split_dataset

def powerFit(x, a, b):      # fitting function for S vs pc - p
    return  b * x**a

def linearFit(x, a, b):     # fitting function for log_S vs log(pc - p)
    return  a*x + b

def fittedArray(x_array, param, choice):
    if choice == "p":
        fitted_array = np.array([ powerFit(x, param[0], param[1]) for x in x_array ])
    elif choice == "l":
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
        p_min = float(input('Minimum Probability (default=0.4): '))
    except ValueError:
        p_min = 0.4

    try:
        p_max = float(input('Maximum Probability (default=0.8): '))
    except ValueError:
        p_max = 0.8

    lx = str(lattice_x)
    ly = str(lattice_y)

    h_array = head_read(lx,ly,p_min,p_max)

    p_step = int(h_array[4])
    num_repeat = int(h_array[5])
    elapsed_time = h_array[6]

    try:
        pc = float(input('Percolation threshold (default=0.6): '))
    except ValueError:
        pc = 0.6

    dataset = file_read(lx,ly,p_min,p_max)
    split_dataset = data_split(dataset, pc)  # p < pcのデータ(p_stepが21なら10個）

    p_array = split_dataset[0]
    dp_array = np.array([ pc - p for p in p_array ])
    log_dp_array = np.log10(dp_array)
    xi_array = split_dataset[1]
    xierr_array = split_dataset[2]
    log_xi_array = split_dataset[3]
    log_xierr_array = split_dataset[4]

    # 以下のslicingはlog-log plotのフィッティングのために行う（必要ない？）
    try:
        slice = input('Use slice? (y or n): ')
    except:
        slice = "n"

    if slice == "y": #範囲を指定するためにスライスを使う場合
        try:
            nump = int(input('Number of points used for fitting (default=5): '))
        except ValueError:
            nump = 5        
        log_dp_array = log_dp_array[-nump:]
        log_xi_array = log_xi_array[-nump:]
        log_xierr_array = log_xierr_array[-nump:]
    else: #範囲を指定するためにスライスを使わない場合
        pass

    param_p, cov_p = curve_fit(powerFit, dp_array, xi_array, sigma=xierr_array)
    err_p = np.sqrt(cov_p[0][0])

    param_l, cov_l = curve_fit(linearFit, log_dp_array, log_xi_array, sigma=log_xierr_array)
    err_l = np.sqrt(cov_l[0][0])

    print('fitting parameter (p < pc): {0}, {1}'.format(param_p[0], err_p))
    print('fitting parameter (log) (p < pc): {0}, {1}'.format(param_l[0], err_l))

    x_array = np.linspace(dp_array[0], dp_array[-1], 100)
    y_array = fittedArray(x_array, param_p, "p")

    logx_array = np.linspace(log_dp_array[0], log_dp_array[-1], 100)
    logy_array = fittedArray(logx_array, param_l, "l")

    fig = plt.figure(figsize=(12,5))

    ax1 = fig.add_subplot(121, title='Correlation Length vs Probability of Occupying Sites', 
            xlabel='$p_{{c}} - p$', ylabel='$ξ$') 
    ax1.grid(visible=True, which='major', color='#666666', linestyle='--')

    ax1.errorbar(dp_array, xi_array, yerr = xierr_array, ls='', marker='o', capsize=5, c=u'#1f77b4')
    ax1.plot(x_array, y_array, c='red')

    ax2 = fig.add_subplot(122, title='Scaling of Correlation Length', 
            xlabel='Log($p_{{c}}$ - $p$)', ylabel='Log($ξ$)')
    ax2.grid(visible=True, which='major', color='#666666', linestyle='--')

    ax2.errorbar(log_dp_array, log_xi_array, yerr = log_xierr_array, ls='', marker='o', capsize=5, c=u'#1f77b4')
    ax2.plot(logx_array, logy_array, c='blue')

    result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
    result_text2 = "Repeat: {}".format(num_repeat)
    result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)
    result_text4 = "$p_{{c}}$ = {}".format(pc)

    fig.text(0.30, 0.80, result_text1)
    fig.text(0.30, 0.75, result_text2)
    fig.text(0.30, 0.70, result_text3)
    fig.text(0.30, 0.65, result_text4)

    resultText_p = "$ξ$ ($p$ < $p_{{c}}$) ∝ ($p_{{c}}$ - $p$)$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(param_p[0], err_p)
    resultText_l = "$ξ$ ($p$ < $p_{{c}}$) ∝ ($p_{{c}}$ - $p$)$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(param_l[0], err_l)
    fig.text(0.30, 0.55, resultText_p)
    fig.text(0.60, 0.15, resultText_l)

    savefile = "./png/clusterStructure_fit_{0}x{1}_p{2}-{3}.png".format(lattice_x,lattice_y, p_min, p_max)
    fig.savefig(savefile, dpi=300)
    
    plt.show()