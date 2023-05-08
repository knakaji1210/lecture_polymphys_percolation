# power_law curve fitting

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

'''
How to use
% python3 curveFit_critical_v2.py args[1] args[2] args[3] args[4] args[5]
args[1] ./data/h_list_100x100_p0.4-0.8.txt
args[2] ./data/p_list_100x100_p0.4-0.8.txt
args[3] ./data/t_list_100x100_p0.4-0.8.txt
args[4] b for a*(pc - x)**b
args[5] b for a*(x - pc)**b
'''

# header read

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

def file_read():

    x_list =[]
    y_list = []

    input_file1 = args[2]
    input_file2 = args[3]

    f=open(input_file1, 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        data = float(datalist[i].rstrip('\n'))
        x_list.append(data)
    f.close()

    f=open(input_file2, 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        data = float(datalist[i].rstrip('\n'))
        y_list.append(data)
    f.close()

    x_array = np.array(x_list)
    y_array = np.array(y_list)
    dataset = [x_array, y_array]

    return dataset

def setROF_L(dataset, pc):
    x_array = [i for i in dataset[0] if i < pc - 0.0001]
    y_array = dataset[1][:len(x_array)]
    cropped_datasetL = [x_array, y_array]
    return cropped_datasetL

def setROF_U(dataset, pc):
    x_array = [i for i in dataset[0] if i > pc + 0.0001]
    y_array = dataset[1][(-1)*len(x_array):]
    cropped_datasetU = [x_array, y_array]
    return cropped_datasetU

def power_fitL(x, a, b):
    return  a*(pc - x)**b

def power_fitU(x, a, b):
    return  a*(x - pc)**b

def fitted_funcL(pc, param, x_array):
    fitted_y_array = [power_fitL(num, param[0], param[1]) for num in x_array]
    return fitted_y_array

def fitted_funcU(pc, param, x_array):
    fitted_y_array = [power_fitU(num, param[0], param[1]) for num in x_array]
    return fitted_y_array

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

 #   guess_p1L = int(args[4])
    guess_p1L = 1.0
    guess_p2L = int(args[4])
 #   guess_p1U = int(args[6])
    guess_p1U = 1.0
    guess_p2U = int(args[5])

    dataset = file_read()
    x_array = dataset[0]
    y_array = dataset[1]
    cropped_datasetL = setROF_L(dataset, pc)
    cropped_x_arrayL = cropped_datasetL[0]
    cropped_y_arrayL = cropped_datasetL[1]
    cropped_datasetU = setROF_U(dataset, pc)
    cropped_x_arrayU = cropped_datasetU[0]
    cropped_y_arrayU = cropped_datasetU[1]

    paramL, covL = curve_fit(power_fitL, cropped_x_arrayL, cropped_y_arrayL, p0=[guess_p1L, guess_p2L])
    paramU, covU = curve_fit(power_fitU, cropped_x_arrayU, cropped_y_arrayU, p0=[guess_p1U, guess_p2U])

    print(paramL)
    print(paramU)
    expL = paramL[1]
    expU = paramU[1]
    expErrL = np.sqrt(covL[1][1])
    expErrU = np.sqrt(covU[1][1])

    x_minL = cropped_x_arrayL[0]
    x_maxL = cropped_x_arrayL[-1]
    x_minU = cropped_x_arrayU[0]
    x_maxU = cropped_x_arrayU[-1]

    fitting_x_arrayL =np.linspace(x_minL, x_maxL, 20)
    fitting_x_arrayU =np.linspace(x_minU, x_maxU, 20)
    fitted_y_arrayL = fitted_funcL(pc, paramL, fitting_x_arrayL)
    fitted_y_arrayU = fitted_funcU(pc, paramU, fitting_x_arrayU)


    fig = plt.figure()

    fig_title = "Fire Extinction Time vs Probability of Green"

    ax = fig.add_subplot(111, title=fig_title, 
            xlabel='$p$', ylabel='$t_{{Extinction}}$')
    ax.grid(b=True, which='major', color='#666666', linestyle='--')
    
    ax.scatter(x_array ,y_array)
#   ax.scatter(cropped_x_arrayL, cropped_y_arrayL, c=u'#1f77b4')
#   ax.scatter(cropped_x_arrayU, cropped_y_arrayU, c=u'#1f77b4')  
    ax.plot(fitting_x_arrayL, fitted_y_arrayL, c='red')
    ax.plot(fitting_x_arrayU, fitted_y_arrayU, c='blue')

    result_text1 = "Lattice: {0} x {1}".format(lattice_x, lattice_y)
    result_text2 = "Repeat: {}".format(num_repeat)
    result_text3 = "$T_{{comp}}$ = {:.2f} s".format(elapsed_time)

    fig.text(0.6, 0.8, result_text1)
    fig.text(0.6, 0.75, result_text2)
    fig.text(0.6, 0.70, result_text3)

    resultTextL = "$t_{{Extinction}}$ ($p$ < $p_{{c}}$) ∝ ($p_{{c}}$ - $p$)$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(expL,expErrL)
    resultTextU = "$t_{{Extinction}}$ ($p$ > $p_{{c}}$) ∝ ($p$ - $p_{{c}}$)$^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(expU,expErrU)
    fig.text(0.15, 0.75, resultTextL)
    fig.text(0.45, 0.15, resultTextU)

    savefile = "./png/forestFire_extinctionTime_fit_{0}x{1}_p{2}-{3}.png".format(lattice_x,lattice_y, p_min, p_max)
    fig.savefig(savefile, dpi=300)
    
    plt.show()