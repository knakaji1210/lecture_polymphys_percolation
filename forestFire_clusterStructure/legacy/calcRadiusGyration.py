# python program to calculate Rg and xi for a given s-cluster

import sys
import numpy as np
import matplotlib.pyplot as plt

'''
How to use
% python3 curveFit_critical_S_v2.py args[1] args[2] args[3] args[4]
'''

# file read

def file_open(input_file):
    data_list = []
    f=open(input_file, 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        data = float(datalist[i].rstrip('\n'))
        data_list.append(data)
    f.close()

    return data_list

def file_read():

    input1 = args[1]
    input2 = args[2]

    coordinate_x = file_open(input1)
    coordinate_y = file_open(input2)
    len_x = len(coordinate_x)
    len_y = len(coordinate_y)
    if len_x == len_y:
        coordinate_list = []
        for i in range(len_x):
            coordinate = [coordinate_x[i], coordinate_y[i]]
            coordinate_list.append(coordinate)
    else:
        pass

    return coordinate_list

def center_mass(coordinate_list):
    s = len(coordinate_list)
    x_list = [ coordinate_list[i][0] for i in range(s) ]
    y_list = [ coordinate_list[i][1] for i in range(s) ]
    center_mass_coordinate = [np.sum(x_list)/s, np.sum(y_list)/s]

    return center_mass_coordinate

def radius_gyration(coordinate_list, center_mass_coordinate):
    s = len(coordinate_list)
    del_x_list = [ coordinate_list[i][0] - center_mass_coordinate[0] for i in range(s) ]
    del_y_list = [ coordinate_list[i][1] - center_mass_coordinate[1] for i in range(s) ]
    d_list = [ del_x_list[i]**2 + del_y_list[i]**2 for i in range(s) ]
    radius_gyration = np.sqrt(np.sum(d_list)/s)

    return radius_gyration

def radius_gyration2(coordinate_list):
    s = len(coordinate_list)
    d2_list = []
    for i in range(s):
        for j in range(s):
            del_x = coordinate_list[i][0] - coordinate_list[j][0]
            del_y = coordinate_list[i][1] - coordinate_list[j][1]
            d2 = del_x**2 + del_y**2
            d2_list.append(d2)
    radius_gyration2 = np.sqrt(np.sum(d2_list)/s**2 /2)

    return radius_gyration2

def calc_dist(coordinate1, coordinate2):
    del_x = coordinate1[0] - coordinate2[0]
    del_y = coordinate1[1] - coordinate2[1]
    dist = np.sqrt(del_x**2 + del_y**2)

    return dist


if __name__ == '__main__':
    args = sys.argv

    coordinate_list= file_read()
    print(coordinate_list)
    s = len(coordinate_list)
    center_mass_coordinate = center_mass(coordinate_list)
    radius_gyration = radius_gyration(coordinate_list, center_mass_coordinate)
#    radius_gyration2 = radius_gyration2(coordinate_list)   # radius_gyrationと同じ値になることを確認ずみ

    result_text1 = "$s$ = {}".format(s)
    result_text2 = "$R_{{s}}$ = {:.2f}".format(radius_gyration)

    fig = plt.figure(figsize=[6,6])

    ax = fig.add_subplot(111,title='Cluster Structure', xlabel='$X$', ylabel='$Y$',
                                             xlim=[-4, 4], ylim=[-4, 4])
    ax.grid(b=True, which='major', color='#999999', linestyle='-')
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    fig.text(0.65, 0.18, result_text1, size=15)
    fig.text(0.65, 0.14, result_text2, size=15)

    for i in range(-4, 4):
        for j in range(-4, 4):
            x = i
            y = j
            coordinate = [x, y]
            if coordinate in coordinate_list:
                ax.plot(x, y, marker="o", color="red", markersize=10)
            else:
#                ax.plot(x, y, marker="o", color="blue")
                pass

    for i in range(s):
        for j in range(s):
            dist = calc_dist(coordinate_list[i], coordinate_list[j])
            if dist <= 1:
                plt.plot([coordinate_list[i][0], coordinate_list[j][0]], [coordinate_list[i][1],coordinate_list[j][1]], color="red",  linewidth=2)

    savefile = "./png/Radius_Gyration_s{}.png".format(s)
    fig.savefig(savefile, dpi=300)

    plt.show()