# log-log curve fitting

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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

    input1 = args[1]
    input2 = args[2]
    input3 = args[3]

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
        fitted_array = [powerFit_u(num, paramset[1][0], paramset[1][1]) for num in x_array]
    elif choice == "l_log":
        fitted_array = [loglogFit(num, logparamset[0][0], logparamset[0][1]) for num in x_array]
    elif choice == "u_log":
        fitted_array = [loglogFit(num, logparamset[1][0], logparamset[1][1]) for num in x_array]
    return fitted_array


if __name__ == '__main__':
    args = sys.argv

    pc = 0.6

    dataset = file_read()
    cropped_setL = setROF(dataset, pc, "l")
    cropped_setU = setROF(dataset, pc, "u")

    logcropped_setL = [[ np.log10(pc - x) for x in cropped_setL[0] ],
                        [ np.log10(y) for y in cropped_setL[1] ]]
    logcropped_setU = [[ np.log10(x - pc) for x in cropped_setU[0] ],
                        [ np.log10(y) for y in cropped_setU[1] ]]

    logcropped_xL = logcropped_setL[0][-4:] #範囲を指定するためにスライスを使う場合
    logcropped_yL = logcropped_setL[1][-4:] #範囲を指定するためにスライスを使う場合
    logcropped_xU = logcropped_setU[0][:4] #範囲を指定するためにスライスを使う場合
    logcropped_yU = logcropped_setU[1][:4] #範囲を指定するためにスライスを使う場合

    param_l, cov_l = curve_fit(powerFit_l, cropped_setL[0], cropped_setL[1])
    param_u, cov_u = curve_fit(powerFit_u, cropped_setU[0], cropped_setU[1])
    paramset = [param_l, param_u]

    #logparam_l, logcov_l = curve_fit(loglogFit, logcropped_setL[0], logcropped_setL[1])
    logparam_l, logcov_l = curve_fit(loglogFit, logcropped_xL, logcropped_yL) #範囲を指定するためにスライスを使う場合
#    logparam_u, logcov_u = curve_fit(loglogFit, logcropped_setU[0], logcropped_setU[1])
    logparam_u, logcov_u = curve_fit(loglogFit, logcropped_xU, logcropped_yU) #範囲を指定するためにスライスを使う場合
    logparamset = [logparam_l, logparam_u]

    print(f'fitting parameter for lower region: {paramset[0]}')
    print(f'fitting parameter for upper region: {paramset[1]}')
    print(f'fitting parameter for lower region: {logparamset[0]}')
    print(f'fitting parameter for upper region: {logparamset[1]}')

    x_arrayL =np.linspace(cropped_setL[0][0], cropped_setL[0][-1], 20)
    x_arrayU =np.linspace(cropped_setU[0][0], cropped_setU[0][-1], 20)
    y_arrayL = fittedArray(x_arrayL, paramset, "l")
    y_arrayU = fittedArray(x_arrayU, paramset, "u")

    logx_arrayL =np.linspace(logcropped_setL[0][0], logcropped_setL[0][-1], 20)
    logx_arrayU =np.linspace(logcropped_setU[0][0], logcropped_setU[0][-1], 20)
    logy_arrayL = fittedArray(logx_arrayL, logparamset, "l_log")
    logy_arrayU = fittedArray(logx_arrayU, logparamset, "u_log")

    fig = plt.figure(figsize=(12,5))


    ax1 = fig.add_subplot(121, title='Mean Correlation Length vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Correlation Length')
    ax1.grid(b=True, which='major', color='#666666', linestyle='--')

    ax1.errorbar(dataset[0], dataset[1], yerr = dataset[2], ls='', marker='o', capsize=5, c=u'#1f77b4')
    ax1.plot(x_arrayL, y_arrayL, c='red')
    #ax1.plot(x_arrayU, y_arrayU, c='yellow')

    ax2 = fig.add_subplot(122, title='Scaling of Correlation Length', 
            xlabel='Log(pc - p)', ylabel='Log(Mean Correlation Length)')
    ax2.grid(b=True, which='major', color='#666666', linestyle='--')

    ax2.scatter(logcropped_setL[0], logcropped_setL[1], marker='o', c=u'#1f77b4')
    #ax2.scatter(logcropped_setU[0], logcropped_setU[1], marker=',', c=u'#1f77b4')
    ax2.plot(logx_arrayL, logy_arrayL, c='blue')
    #ax2.plot(logx_arrayU, logy_arrayU)

    resultTextL = "ξ (p < pc) ∝ (pc - p)^("+str(round(paramset[0][1],2))+")"
    resultTextU = "P (p > pc) ∝ (p - pc)^("+str(round(paramset[1][1],2))+")"
    resultTextlogL = "ξ (p < pc) ∝ (pc - p)^("+str(round(logparamset[0][0],2))+")"
    resultTextlogU = "P (p > pc) ∝ (p - pc)^("+str(round(logparamset[1][0],2))+")"
    fig.text(0.30, 0.17, resultTextL)
    #fig.text(0.30, 0.15, resultTextU)
    fig.text(0.57, 0.25, resultTextlogL)
    #fig.text(0.72, 0.70, resultTextlogU)

    fig.savefig("./png/corr_length_mean_fit.png", dpi=300)
    
    plt.show()