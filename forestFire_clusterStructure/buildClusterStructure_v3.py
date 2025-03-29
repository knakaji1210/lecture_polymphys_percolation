# cluster statistics

# 250329コメント
# importしていたcalcClusterAttribute_v2をそのままこちらにコピペして一体化させた
# 従って、calcClusterAttribute_v2はレガシーに移動した

import numpy as np
import clusterFunc_rg as crg

'''
calcClusterAttributeについて
引数はcluster_coordinatesであり、これはある1つのクラスターに属すsitesの座標のリストで
[[-4.5, -0.5], [-4.5, 0.5], [-3.5, -0.5], [-4.5, 1.5], [-4.5, 2.5], [-4.5, 3.5], [-4.5, 4.5], [-3.5, 3.5], [-3.5, 4.5]]
のようなもの。ここからsとradius_gyrationを計算して、それを返り値として渡す関数
'''

def calcClusterAttribute(cluster_coordinates):

#    print(cluster_coordinates)

    s = len(cluster_coordinates)        # number of occupied sites in this cluster

    x_coordinates = [ cluster_coordinates[i][0] for i in range(s) ]
    y_coordinates = [ cluster_coordinates[i][1] for i in range(s) ]
    var_x = np.var(x_coordinates)       # 分散
    var_y = np.var(y_coordinates)
    radius_gyration = np.sqrt(var_x + var_y)
    cluster_attribute = [ s, radius_gyration ]

    return cluster_attribute

'''
buildClusterStructureについて
これはforestFire_clusterSizeのclusterFuncResult_rg.pyのbuildClusterListをベースに作成
buildClusterListの返り値はclusters_list（sのリスト）で、例えば
[1, 2, 5, 5, 25, 6, 2, 1, 1, 1, 26, 1, 5, 1, 1, 1, 46, 54, 1, 13, 1, 1, 1, 1, 1, 5, 1, 1, 1, 2, 10, 1, 1, 2, 70, 53, 1, 1, 1, 7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 5, 3, 1, 1, 1, 5, 3, 1, 2, 12, 2, 1, 9, 1, 1, 1, 1, 3, 3, 12, 10, 1, 2, 1, 1]
のようなリスト。buildClusterStructureでは返り値を
cluster_attribute_list（[s, radius_gyration]のリスト）に変更
例えば
[[1, 0.0], [1, 0.0], [1, 0.0], [1, 0.0], [1, 0.0], [1, 0.0], [2, 0.5], [2, 0.5], [5, 0.9797958971132713], [5, 1.058300524425836], [7, 1.124858267715973], [8, 1.7320508075688772], [10, 1.5652475842498528]]
のようなリスト。要素数を数えればclusters_listは再構成できる
'''

def buildClusterStructure(lattice_x, lattice_y, p):
 
        end_point_id = lattice_x * lattice_y

# Building of initial configuration

        initialConfig = crg.initialConfig(lattice_x, lattice_y, p)
        greenCount = crg.greenCount(end_point_id, initialConfig)

# Setting a firing point

        num_steps = 0
        cluster_attribute_list = []

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
                        cluster_coordinates += cluster_coordinates_diff #cluster structureのために追加
                        currentConfig = updatedConfig
                cluster_coordinates.insert(0, int_fired_point_coordinate) #cluster structureのために追加
                cluster_attribute = calcClusterAttribute(cluster_coordinates)
                cluster_attribute_list.append(cluster_attribute) #cluster structureのために追加
                cluster_attribute_list.sort()

        return cluster_attribute_list
