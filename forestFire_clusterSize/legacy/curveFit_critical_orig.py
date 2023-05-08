# log-log curve fitting

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# file read

def file_read():

    x_list =[]
    y_list = []
    yerr_list = []

    input_file1 = args[1]
    input_file2 = args[2]
    input_file3 = args[3]

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

    f=open(input_file3, 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        data = float(datalist[i].rstrip('\n'))
        yerr_list.append(data)
    f.close()

    x_array = np.array(x_list)
    y_array = np.array(y_list)
    yerr_array = np.array(yerr_list)
    dataset = [x_array, y_array, yerr_array]

    return dataset

def setROF_L(dataset, pc):
    x_array = [i for i in dataset[0] if round(i,2) < pc]
    y_array = dataset[1][:len(x_array)]
    yerr_array = dataset[2][:len(x_array)]
    cropped_datasetL = [x_array, y_array, yerr_array]
    return cropped_datasetL

def setROF_U(dataset, pc):
    x_array = [i for i in dataset[0] if round(i,2) > pc]
    y_array = dataset[1][(-1)*len(x_array):]
    yerr_array = dataset[2][(-1)*len(x_array):]
    cropped_datasetU = [x_array, y_array, yerr_array]
    return cropped_datasetU

def power_fitL(x, a, b):
    return  a*(pc - x)**b

def power_fitU(x, a, b):
    return  a*(x - pc)**b

def loglog_fit(x, a, b):
    return  a*x + b  

def fitted_funcL(pc, param, x_array):
    fitted_y_array = [power_fitL(num, param[0], param[1]) for num in x_array]
    return fitted_y_array

def fitted_funcU(pc, param, x_array):
    fitted_y_array = [power_fitU(num, param[0], param[1]) for num in x_array]
    return fitted_y_array

def fitted_func_log(param, x_array):
    fitted_y_array = [loglog_fit(num, param[0], param[1]) for num in x_array]
    return fitted_y_array

if __name__ == '__main__':
    args = sys.argv

    pc = 0.6
    #guess_p1L = int(args[4])
    #guess_p2L = int(args[5])
    #guess_p1U = int(args[6])
    #guess_p2U = int(args[7])
    guess_p1L = 1
    guess_p2L = 1
    guess_p1U = 1
    guess_p2U = 1

    dataset = file_read()
    x_array = dataset[0]
    y_array = dataset[1]
    yerr_array = dataset[2]
    cropped_datasetL = setROF_L(dataset, pc)
    cropped_x_arrayL = cropped_datasetL[0]
    cropped_y_arrayL = cropped_datasetL[1]
    cropped_datasetU = setROF_U(dataset, pc)
    cropped_x_arrayU = cropped_datasetU[0]
    cropped_y_arrayU = cropped_datasetU[1]
    
#    log_cropped_x_arrayL = [ np.log10(x) for x in cropped_x_arrayL ]
#    log_cropped_y_arrayL = [ np.log10(y) for y in cropped_y_arrayL ]

    paramL, covL = curve_fit(power_fitL, cropped_x_arrayL, cropped_y_arrayL, p0=[guess_p1L, guess_p2L])
    paramU, covU = curve_fit(power_fitU, cropped_x_arrayU, cropped_y_arrayU, p0=[guess_p1U, guess_p2U])
    print(paramL)
    print(paramU)

    x_minL = cropped_x_arrayL[0]
    x_maxL = cropped_x_arrayL[-1]
    x_minU = cropped_x_arrayU[0]
    x_maxU = cropped_x_arrayU[-1]

    fitting_x_arrayL =np.linspace(x_minL, x_maxL, 20)
    fitting_x_arrayU =np.linspace(x_minU, x_maxU, 20)
    fitted_y_arrayL = fitted_funcL(pc, paramL, fitting_x_arrayL)
    fitted_y_arrayU = fitted_funcU(pc, paramU, fitting_x_arrayU)


    fig = plt.figure()


    ax1 = fig.add_subplot(111, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Cluster Size')
    ax1.grid(b=True, which='major', color='#666666', linestyle='--')

    ax1.errorbar(x_array, y_array, yerr = yerr_array, ls='', marker='o', capsize=5)
#    ax1.scatter(cropped_x_arrayL, cropped_y_arrayL, c=u'#1f77b4')
#    ax1.scatter(cropped_x_arrayU, cropped_y_arrayU, c=u'#1f77b4')  

    ax1.plot(fitting_x_arrayL, fitted_y_arrayL, c='red')
    ax1.plot(fitting_x_arrayU, fitted_y_arrayU, c='blue')


#    ax.scatter(log_cropped_x_arrayL, log_cropped_y_arrayL, c=u'#1f77b4')



    resultTextL = "S (p < pc) ∝ (pc - p)^("+str(round(paramL[1],2))+")"
    resultTextU = "S (p > pc) ∝ (p - pc)^("+str(round(paramU[1],2))+")"
    fig.text(0.15, 0.75, resultTextL)
    fig.text(0.55, 0.15, resultTextU)

    fig.savefig("./png/cluster_size_mean_fit.png", dpi=300)
    
    plt.show()