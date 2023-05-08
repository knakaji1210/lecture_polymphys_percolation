# curve fitting for cluster size (p > pc)

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

'''
How to use
% python3 curveFit_critical_P_v2.py args[1] args[2] args[3] args[4]
args[1] ./data/h_list_100x100_p0.4-0.8.txt
args[2] ./data/p_list_100x100_p0.4-0.8.txt
args[3] ./data/P_mean_list_100x100_p0.4-0.8.txt
args[4] ./data/P_std_list_100x100_p0.4-0.8.txt
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

    x_array = np.array(file_open(input1))
    y_array = np.array(file_open(input2))
    yerr_array = np.array(file_open(input3))
    dataset = [x_array, y_array, yerr_array]

    return dataset

def setROF(dataset, pc, choice):
    if choice == "l":
        x_array = [i for i in dataset[0] if round(i,2) < pc]
        y_array = dataset[1][:len(x_array)]
        yerr_array = dataset[2][:len(x_array)]
    elif choice == "u":
        x_array = [i for i in dataset[0] if round(i,2) > pc]
        y_array = dataset[1][(-1)*len(x_array):]
        yerr_array = dataset[2][(-1)*len(x_array):]
    cropped_dataset = [x_array, y_array, yerr_array]
    return cropped_dataset

def powerFit_l(x, a, b):
    return  a*(pc - x)**b

def powerFit_u(x, a, b):
    return  a*(x - pc)**b

def loglogFit(x, a, b):
    return  a*(x - pc) + b

def fittedArray(x_array, paramset, choice):
    if choice == "l":
        fitted_array = [powerFit_l(num, paramset[0][0], paramset[0][1]) for num in x_array]
    elif choice == "u":
        fitted_array = [powerFit_u(num, paramset[2][0], paramset[2][1]) for num in x_array]
    elif choice == "l_log":
        fitted_array = [loglogFit(num, logparamset[0][0], logparamset[0][1]) for num in x_array]
    elif choice == "u_log":
        fitted_array = [loglogFit(num, logparamset[2][0], logparamset[2][1]) for num in x_array]
    return fitted_array


if __name__ == '__main__':
    args = sys.argv

    h_array = head_read()

    lattice_x = int(h_array[0])
    lattice_y = int(h_array[1])
    p_min = h_array[2]
    p_max = h_array[3]
    p_step = int(h_array[4])
    num_repeat = int(h_array[5])
    elapsed_time = h_array[6]

    try:
        pc = float(input('Percolation threshold (default=0.6): '))
    except ValueError:
        pc = 0.6

    dataset = file_read()
    cropped_setL = setROF(dataset, pc, "l")
    cropped_setU = setROF(dataset, pc, "u")

    try:
        slice = input('Use slice? (y or n): ')
    except:
        slice = "n"

    logcropped_setL = [[ np.log10(pc - x) for x in cropped_setL[0] ],
                        [ np.log10(y) for y in cropped_setL[1] ]]
    logcropped_setU = [[ np.log10(x - pc) for x in cropped_setU[0] ],
                        [ np.log10(y) for y in cropped_setU[1] ]]

    if slice == "y": #範囲を指定するためにスライスを使う場合
        try:
            dp = int(input('Number of points used for fitting (default=3): '))
        except ValueError:
            dp = 3        
        logcropped_xL = logcropped_setL[0][-dp:]
        logcropped_yL = logcropped_setL[1][-dp:]
        logcropped_xU = logcropped_setU[0][:dp]
        logcropped_yU = logcropped_setU[1][:dp]
    else: #範囲を指定するためにスライスを使わない場合
        logcropped_xL = logcropped_setL[0] 
        logcropped_yL = logcropped_setL[1]
        logcropped_xU = logcropped_setU[0]
        logcropped_yU = logcropped_setU[1]

    param_l, cov_l = curve_fit(powerFit_l, cropped_setL[0], cropped_setL[1])
    param_u, cov_u = curve_fit(powerFit_u, cropped_setU[0], cropped_setU[1])
    err_l = np.sqrt(cov_l[1][1])
    err_u = np.sqrt(cov_u[1][1])
    paramset = [param_l, err_l, param_u, err_u]

    logparam_l, logcov_l = curve_fit(loglogFit, logcropped_xL, logcropped_yL)
    logparam_u, logcov_u = curve_fit(loglogFit, logcropped_xU, logcropped_yU)
    logerr_l = np.sqrt(logcov_l[1][1])
    logerr_u = np.sqrt(logcov_u[1][1])
    logparamset = [logparam_l, logerr_l, logparam_u, logerr_u]

#    print('fitting parameter (p < pc): {}'.format(paramset[0]))
    print('fitting parameter (p > pc): {}'.format(paramset[2]))
#    print('fitting parameter (log) (p < pc): {}'.format(logparamset[0]))
    print('fitting parameter (log) (p > pc): {}'.format(logparamset[2]))

#    x_arrayL =np.linspace(cropped_setL[0][0], cropped_setL[0][-1], 20)
    x_arrayU =np.linspace(cropped_setU[0][0], cropped_setU[0][-1], 20)
#    y_arrayL = fittedArray(x_arrayL, paramset, "l")
    y_arrayU = fittedArray(x_arrayU, paramset, "u")

#    logx_arrayL =np.linspace(logcropped_setL[0][0], logcropped_setL[0][-1], 20)
    logx_arrayU =np.linspace(logcropped_setU[0][0], logcropped_setU[0][-1], 20)
#    logy_arrayL = fittedArray(logx_arrayL, logparamset, "l_log")
    logy_arrayU = fittedArray(logx_arrayU, logparamset, "u_log")

    fig = plt.figure(figsize=(12,5))


    ax1 = fig.add_subplot(121, title='Percolation Cluster Size vs Probability of Occupying Sites', 
            xlabel='$p$', ylabel='$P$')
    ax1.grid(visible=True, which='major', color='#666666', linestyle='--')

    ax1.errorbar(dataset[0], dataset[1], yerr = dataset[2], ls='', marker='o', capsize=5, c=u'#1f77b4')
    ax1.plot(x_arrayU, y_arrayU, c='red')

    ax2 = fig.add_subplot(122, title='Scaling of Percolation Cluster Size', 
            xlabel='Log($p$ - $p_{{c}}$)', ylabel='Log($P$)')
    ax2.grid(visible=True, which='major', color='#666666', linestyle='--')

    ax2.scatter(logcropped_setU[0], logcropped_setU[1], marker=',', c=u'#1f77b4')
    ax2.plot(logx_arrayU, logy_arrayU,  c='blue')

    result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
    result_text2 = "Repeat: {}".format(num_repeat)
    result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)
    result_text4 = "$p_{{c}}$ = {}".format(pc)

    fig.text(0.15, 0.8, result_text1)
    fig.text(0.15, 0.75, result_text2)
    fig.text(0.15, 0.70, result_text3)
    fig.text(0.15, 0.65, result_text4)

    resultTextU = "$P$ ($p$ > $p_{{c}}$) ∝ ($p$ - $p_{{c}}$)$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(paramset[2][1], paramset[3])
    resultTextlogU = "$P$ ($p$ > $p_{{c}}$) ∝ ($p$ - $p_{{c}}$)$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(logparamset[2][0],logparamset[3])
    fig.text(0.30, 0.17, resultTextU)
    fig.text(0.62, 0.17, resultTextlogU)

    savefile = "./png/clusterSize_P_fit_{0}x{1}_p{2}-{3}.png".format(lattice_x,lattice_y, p_min, p_max)
    fig.savefig(savefile, dpi=300)
    
    plt.show()