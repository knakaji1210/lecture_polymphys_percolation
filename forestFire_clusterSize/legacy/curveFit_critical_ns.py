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

    x_array = np.array(file_open(input1))
    y_array = np.array(file_open(input2))
    dataset = [x_array, y_array]

    return dataset

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

    dataset_orig = file_read()

    dataset = remove_inf(dataset_orig)

    param, cov = curve_fit(loglogFit, dataset[0], dataset[1])

    print(f'fitting parameter: {param}')

    x_array =np.linspace(dataset[0][0], dataset[0][-1], 20)
    y_array = fittedArray(x_array, param)

    fig = plt.figure()

    ax = fig.add_subplot(111, title='Scaling of Number of s-cluster', 
            xlabel='Log(s)', ylabel='Log(n_s)')
    ax.grid(b=True, which='major', color='#666666', linestyle='--')

    ax.scatter(dataset[0], dataset[1], marker='o', c=u'#1f77b4')
    ax.plot(x_array, y_array,  c='blue')

    resultText = "n_s (pc) ∝ tau^("+str(round(param[0],3))+")"
    fig.text(0.50, 0.7, resultText)

    fig.savefig("./png/nspc_fit.png", dpi=300)
    
    plt.show()