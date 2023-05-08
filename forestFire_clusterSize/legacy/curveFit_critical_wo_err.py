# power_law curve fitting

import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# file read

def file_read():

    x_list =[]
    y_list = []

    input_file1 = args[1]
    input_file2 = args[2]

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
    x_array = [i for i in dataset[0] if i < pc]
    y_array = dataset[1][:len(x_array)]
    cropped_datasetL = [x_array, y_array]
    return cropped_datasetL

def setROF_U(dataset, pc):
    x_array = [i for i in dataset[0] if i > pc]
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

    pc = 0.6
    guess_p1L = int(args[3])
    guess_p2L = int(args[4])
#    guess_p1U = int(args[5])
#    guess_p2U = int(args[6])

    dataset = file_read()
    x_array = dataset[0]
    y_array = dataset[1]
    cropped_datasetL = setROF_L(dataset, pc)
    cropped_x_arrayL = cropped_datasetL[0]
    cropped_y_arrayL = cropped_datasetL[1]
#    cropped_datasetU = setROF_U(dataset, pc)
#    cropped_x_arrayU = cropped_datasetU[0]
#    cropped_y_arrayU = cropped_datasetU[1]
    
    paramL, covL = curve_fit(power_fitL, cropped_x_arrayL, cropped_y_arrayL, p0=[guess_p1L, guess_p2L])
#    paramU, covU = curve_fit(power_fitU, cropped_x_arrayU, cropped_y_arrayU, p0=[guess_p1U, guess_p2U])
    print(paramL)
#    print(paramU)

    x_minL = cropped_x_arrayL[0]
    x_maxL = cropped_x_arrayL[-1]
#    x_minU = cropped_x_arrayU[0]
#    x_maxU = cropped_x_arrayU[-1]

    fitting_x_arrayL =np.linspace(x_minL, x_maxL, 20)
#    fitting_x_arrayU =np.linspace(x_minU, x_maxU, 20)
    fitted_y_arrayL = fitted_funcL(pc, paramL, fitting_x_arrayL)
#    fitted_y_arrayU = fitted_funcU(pc, paramU, fitting_x_arrayU)


    fig = plt.figure()

    ax = fig.add_subplot(111, title='Mean Cluster Size vs Probability of Occupying Sites', 
            xlabel='Probability of Occupying Sites', ylabel='Mean Cluster Size')
    ax.grid(b=True, which='major', color='#666666', linestyle='--')

    ax.scatter(cropped_x_arrayL, cropped_y_arrayL, c=u'#1f77b4')
#    ax.scatter(cropped_x_arrayU, cropped_y_arrayU, c=u'#1f77b4')  
    #ax.scatter(x_array ,y_array)
    ax.plot(fitting_x_arrayL, fitted_y_arrayL, c='red')
#    ax.plot(fitting_x_arrayU, fitted_y_arrayU, c='blue')
    resultTextL = "S (p < pc) ∝ (pc - p)^("+str(round(paramL[1],2))+")"
#    resultTextU = "T (p > pc) ∝ (p - pc)^("+str(round(paramU[1],2))+")"
    fig.text(0.15, 0.75, resultTextL)
#    fig.text(0.55, 0.15, resultTextU)

    fig.savefig("./png/cluster_size_mean_fit.png", dpi=300)
    
    plt.show()