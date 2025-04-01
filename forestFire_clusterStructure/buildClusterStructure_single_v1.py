# cluster statistics

# 250329コメント
# 指定したsに対するcluster_attributeを返すプログラム
# 250401コメント
# calcRadiusGyration_v3.py
# でファイル書き出しなどしないでそのまま描画まで進むバージョンができたので、
# こちらの
# if __name__ == '__main__':
# 以降は不要（一応残しておくが・・・）


import random
import numpy as np
import clusterFunc_rg as crg

'''
calcClusterAttribute(single用に修正している)について
引数はcluster_coordinatesであり、これはある1つのクラスターに属すsitesの座標のリストで
[[-4.5, -0.5], [-4.5, 0.5], [-3.5, -0.5], [-4.5, 1.5], [-4.5, 2.5], [-4.5, 3.5], [-4.5, 4.5], [-3.5, 3.5], [-3.5, 4.5]]
のようなもの。ここからx_coordinatesとy_coordinatesとradius_gyrationを計算して、それを返り値として渡す関数
'''

def buildClusterStructure(lattice_x, lattice_y, p):
 
        end_point_id = lattice_x * lattice_y

# Building of initial configuration

        initialConfig = crg.initialConfig(lattice_x, lattice_y, p)
        greenCount = crg.greenCount(end_point_id, initialConfig)

# Setting a firing point

        num_steps = 0
        cluster_coordinates_list = []

        while greenCount > 0:
                fireCount = 0
                while fireCount == 0:
                        currentConfig, int_fired_point_coordinate = crg.initialFire(end_point_id, initialConfig)
                        fireCount = crg.fireCount(end_point_id, currentConfig)
                
# Stepwise fire spreading
                cluster_coordinates = []
                while fireCount > 0:
                        num_steps+=1
#                       pointsCoordinates = crg.pointsCoordinates(end_point_id, currentConfig)　# 描画には必要だが、ここでは不要
                        fireCount = crg.fireCount(end_point_id, currentConfig)
                        greenCount = crg.greenCount(end_point_id, currentConfig)
                        updatedConfig, cluster_coordinates_diff = crg.fireSpread(lattice_x, lattice_y, end_point_id, currentConfig) #cluster structureのために変更
                        cluster_coordinates += cluster_coordinates_diff         # cluster structureのために追加
                        currentConfig = updatedConfig
                cluster_coordinates.insert(0, int_fired_point_coordinate)       # cluster structureのために追加
                cluster_coordinates_list.append(cluster_coordinates)            # cluster structure (single用)のために追加
                cluster_coordinates_list.sort()                                 # cluster structure (single用)のために追加

        return cluster_coordinates_list

def calcCoordinateList(cluster_coordinates):                              # 重心位置を原点付近に平行移動させる関数 

        s = len(cluster_coordinates)
        x_list = [ cluster_coordinates[i][0] for i in range(s) ]
        y_list = [ cluster_coordinates[i][1] for i in range(s) ]
        center_mass_coordinate = [np.sum(x_list)/s, np.sum(y_list)/s]
        new_x_list = [ x_list[i] - round(center_mass_coordinate[0]) - 0.5 for i in range(s) ]   # '- 0.5'はx, y座標を整数化するため
        new_y_list = [ y_list[i] - round(center_mass_coordinate[1]) - 0.5 for i in range(s) ]
        coordinate_list = [ new_x_list, new_y_list ]

        return coordinate_list

def calcClusterAttribute(cluster_coordinates):

    s = len(cluster_coordinates)        # number of occupied sites in this cluster

    x_list = [ cluster_coordinates[i][0] for i in range(s) ]
    y_list = [ cluster_coordinates[i][1] for i in range(s) ]
    var_x = np.var(x_list)       # 分散
    var_y = np.var(y_list)
    radius_gyration = np.sqrt(var_x + var_y)
    cluster_attribute = [ s, radius_gyration ]

    return cluster_attribute

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

        cluster_coordinates_list = buildClusterStructure(lattice_x, lattice_y, p)
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
        coordinate_list = calcCoordinateList(cluster_coordinates)
        cluster_attribute = calcClusterAttribute(cluster_coordinates)
        print(cluster_attribute)

        savefile1 = "./data/coordinate_x_s{0}.txt".format(s)
        savefile2 = "./data/coordinate_y_s{0}.txt".format(s)
        savefile3 = "./data/cluster_attribute_s{0}.txt".format(s)

        np.savetxt(savefile1, coordinate_list[0])
        np.savetxt(savefile2, coordinate_list[1])
        np.savetxt(savefile3, cluster_attribute)


