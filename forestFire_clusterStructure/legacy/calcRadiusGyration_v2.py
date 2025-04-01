# python program to calculate Rg and xi for a given s-cluster

# 250401コメント
# v3でファイル書き出ししなくてよいバージョンができたのでレガシーに移動

import sys
import numpy as np
import matplotlib.pyplot as plt

'''
How to use
% python3 calcRadiusGyration_v2.py args[1] args[2]
args[1] = ./data/coordinate_x_s15.txt
args[2] = ./data/coordinate_y_s15.txt
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
    max_x = np.max(np.abs(coordinate_x))
    print('max_x = ', max_x)
    max_y = np.max(np.abs(coordinate_y))
    print('max_y = ', max_y)
    max_coordinate = np.max([ max_x, max_y ])
    print('max_coordinate = ', max_coordinate)
    if len_x == len_y:
        cluster_coordinates = []
        for i in range(len_x):
            coordinate = [coordinate_x[i], coordinate_y[i]]
            cluster_coordinates.append(coordinate)
    else:
        pass

    return cluster_coordinates, max_coordinate

def center_mass(cluster_coordinates):
    s = len(cluster_coordinates)
    x_list = [ cluster_coordinates[i][0] for i in range(s) ]
    y_list = [ cluster_coordinates[i][1] for i in range(s) ]
    center_mass_coordinate = [np.sum(x_list)/s, np.sum(y_list)/s]

    return center_mass_coordinate

def calcRadiusGyration1(cluster_coordinates, center_mass_coordinate):
    s = len(cluster_coordinates)
    del_x_list = [ cluster_coordinates[i][0] - center_mass_coordinate[0] for i in range(s) ]
    del_y_list = [ cluster_coordinates[i][1] - center_mass_coordinate[1] for i in range(s) ]
    d_list = [ del_x_list[i]**2 + del_y_list[i]**2 for i in range(s) ]
    radius_gyration = np.sqrt(np.sum(d_list)/s)

    return radius_gyration

def calcRadiusGyration2(cluster_coordinates):
    s = len(cluster_coordinates)
    d2_list = []
    for i in range(s):
        for j in range(s):
            del_x = cluster_coordinates[i][0] - cluster_coordinates[j][0]
            del_y = cluster_coordinates[i][1] - cluster_coordinates[j][1]
            d2 = del_x**2 + del_y**2
            d2_list.append(d2)
    radius_gyration2 = np.sqrt(np.sum(d2_list)/s**2 /2)

    return radius_gyration2

def calcRadiusGyration3(cluster_coordinates):

    s = len(cluster_coordinates)        # number of occupied sites in this cluster

    x_coordinates = [ cluster_coordinates[i][0] for i in range(s) ]
    y_coordinates = [ cluster_coordinates[i][1] for i in range(s) ]
    var_x = np.var(x_coordinates)       # 分散
    var_y = np.var(y_coordinates)
    radius_gyration3 = np.sqrt(var_x + var_y)

    return radius_gyration3

def calcDist(coordinate1, coordinate2):
    del_x = coordinate1[0] - coordinate2[0]
    del_y = coordinate1[1] - coordinate2[1]
    dist = np.sqrt(del_x**2 + del_y**2)

    return dist


if __name__ == '__main__':
    args = sys.argv

    cluster_coordinates, max_coordinate = file_read()
    print(cluster_coordinates)
    s = len(cluster_coordinates)
    print('s = ', s)
    center_mass_coordinate = center_mass(cluster_coordinates)
    radius_gyration1 = calcRadiusGyration1(cluster_coordinates, center_mass_coordinate)
    radius_gyration2 = calcRadiusGyration2(cluster_coordinates)     # radius_gyration1と同じ値になることを確認ずみ
    radius_gyration3 = calcRadiusGyration3(cluster_coordinates)     # radius_gyration1と同じ値になることを確認ずみ
    print('Rg_1 = ', radius_gyration1)
    print('Rg_2 = ', radius_gyration2)
    print('Rg_3 = ', radius_gyration3)

    result_text1 = "$s$ = {}".format(s)
    result_text2 = "$R_{{s}}$ = {:.2f}".format(radius_gyration1)

    max_range = int(max_coordinate + 2)
    print(max_range)

    fig = plt.figure(figsize=[6,6])

    ax = fig.add_subplot(111,title='Cluster Structure', xlabel='$X$', ylabel='$Y$',
                                             xlim=[-max_range, max_range], ylim=[-max_range, max_range])
    ax.grid(visible=True, which='major', color='#999999', linestyle='-')
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    fig.text(0.65, 0.18, result_text1, size=15)
    fig.text(0.65, 0.14, result_text2, size=15)

    for i in range(-max_range, max_range):          # 範囲指定した格子点上全てについてそこにクラスター上の点があるかを調べている
        for j in range(-max_range, max_range):
            x = i
            y = j
            coordinate = [x, y]
            if coordinate in cluster_coordinates:
                ax.plot(x, y, marker="o", color="red", markersize=10)
            else:
#                ax.plot(x, y, marker="o", color="blue")
                pass

    for i in range(s):
        for j in range(s):
            dist = calcDist(cluster_coordinates[i], cluster_coordinates[j])
            if dist <= 1:
                plt.plot([cluster_coordinates[i][0], cluster_coordinates[j][0]], [cluster_coordinates[i][1],cluster_coordinates[j][1]], color="red",  linewidth=2)

    savefile = "./png/Radius_Gyration_s{}.png".format(s)
    fig.savefig(savefile, dpi=300)

    plt.show()