# python program to calculate Rg and xi for a given s-cluster

import random
import numpy as np
import matplotlib.pyplot as plt
import buildClusterStructure_single_v1 as bcss

# 250331コメント
# buildClusterStructure_single_v1.py
# をインポートし、そのままRgの計算を行うバージョン
# 従って、ファイル読み込みはしない

def coordinate_list2cluster_coordinates(coordinate_list):

    x_list = coordinate_list[0]
    y_list = coordinate_list[1]
    len_x = len(x_list)
    len_y = len(y_list)
    max_x = np.max(np.abs(x_list))
    max_y = np.max(np.abs(y_list))
    max_coordinate = np.max([ max_x, max_y ])
    if len_x == len_y:
        cluster_coordinates = []
        for i in range(len_x):
            coordinate = [x_list[i], y_list[i]]
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

    try:
        lattice_x = int(input('X-Lattice Size (default=100): '))
    except ValueError:
        lattice_x = 100

    try:
        lattice_y = int(input('Y-Lattice Size (default=100): '))
    except ValueError:
        lattice_y = 100

    try:
        p = float(input('Probability (default=0.5): '))
    except ValueError:
        p = 0.5

    try:
        s = int(input('Cluster size (default=15): '))
    except ValueError:
        s = 15

    end_point_id = lattice_x * lattice_y

    cluster_coordinates_list = bcss.buildClusterStructure(lattice_x, lattice_y, p)
    num_clusters = len(cluster_coordinates_list)

    selected_cluster_cooridinates_list = []

    for i in range(num_clusters):
        s_inList = len(cluster_coordinates_list[i])
        if s_inList == s:
                selected_cluster_coordinates = cluster_coordinates_list[i]
                selected_cluster_cooridinates_list.append(selected_cluster_coordinates)
        else:
            pass
        
    cluster_coordinates = random.choice(selected_cluster_cooridinates_list)
    coordinate_list = bcss.calcCoordinateList(cluster_coordinates)
    cluster_attribute = bcss.calcClusterAttribute(cluster_coordinates)
    updated_cluster_coordinates, max_coordinate = coordinate_list2cluster_coordinates(coordinate_list)
    cluster_attribute = bcss.calcClusterAttribute(cluster_coordinates)

    center_mass_coordinate = center_mass(cluster_coordinates)
    radius_gyration1 = calcRadiusGyration1(cluster_coordinates, center_mass_coordinate)
    radius_gyration2 = calcRadiusGyration2(cluster_coordinates)     # radius_gyration1と同じ値になることを確認ずみ
    radius_gyration3 = calcRadiusGyration3(cluster_coordinates)     # radius_gyration1と同じ値になることを確認ずみ
    print('Rg_1 = ', radius_gyration1)
    print('Rg_2 = ', radius_gyration2)
    print('Rg_3 = ', radius_gyration3)

    result_text1 = "$s$ = {}".format(s)
    result_text2 = "$R_{{s}}$ = {:.2f}".format(radius_gyration1)

    max_range = round(np.sqrt(s))*1.5

    fig = plt.figure(figsize=[6,6])

    ax = fig.add_subplot(111,title='Cluster Structure', xlabel='$X$', ylabel='$Y$',
                                             xlim=[-max_range, max_range], ylim=[-max_range, max_range])
    ax.grid(visible=True, which='major', color='#999999', linestyle='-')
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    fig.text(0.65, 0.18, result_text1, size=15)
    fig.text(0.65, 0.14, result_text2, size=15)

    max_lattice = int(max_coordinate + 2)

    for i in range(-max_lattice, max_lattice):          # 範囲指定した格子点上全てについてそこにクラスター上の点があるかを調べている
        for j in range(-max_lattice, max_lattice):
            x = i
            y = j
            coordinate = [x, y]
            if coordinate in updated_cluster_coordinates:
                ax.plot(x, y, marker="o", color="red", markersize=10)
            else:
#                ax.plot(x, y, marker="o", color="blue")
                pass

    for i in range(s):
        for j in range(s):
            dist = calcDist(updated_cluster_coordinates[i], updated_cluster_coordinates[j])
            if dist <= 1:
                plt.plot([updated_cluster_coordinates[i][0], updated_cluster_coordinates[j][0]], [updated_cluster_coordinates[i][1],updated_cluster_coordinates[j][1]], color="red",  linewidth=2)

    savefile = "./png/Radius_Gyration_s{0}_Rg{1:.2f}.png".format(s,radius_gyration1)
    fig.savefig(savefile, dpi=300)

    plt.show()