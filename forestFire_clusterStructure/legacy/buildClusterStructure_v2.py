# cluster statistics

import clusterFunc_rg as crg
import calcClusterAttribute_v2 as cca

'''
buildClusterListをベースに作成、返り値をclusters_list（sのリスト）から
cluster_str_list（各クラスターに属すsitesの座標のリスト）に変更
sitesの数を数えればclusters_listは再構成できる

さらにcluster_strからradius_gyrationを計算して、それを返り値として渡すことにする
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
                cluster_attribute = cca.calcClusterAttribute(cluster_coordinates)
                cluster_attribute_list.append(cluster_attribute) #cluster structureのために追加
                cluster_attribute_list.sort()

        return cluster_attribute_list
