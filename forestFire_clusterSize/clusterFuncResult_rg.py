# cluster statistics

import clusterFunc_rg as crg
# import clusterStat as cs

def buildClusterList(lattice_x, lattice_y, p):

        end_point_id = lattice_x * lattice_y

        num_repeat = 0

# Building of initial configuration

        initialConfig = crg.initialConfig(lattice_x, lattice_y, p)
        greenCount = crg.greenCount(end_point_id, initialConfig)

# Setting a firing point

        num_steps = 0
        clusters_list = []

        while greenCount > 0:
                fireCount = 0
                while fireCount == 0:
                        currentConfig = crg.initialFire(end_point_id, initialConfig)
                        fireCount = crg.fireCount(end_point_id, currentConfig)
                
# Stepwise fire spreading
                num_occupied_sites = 0
                while fireCount > 0:
                        num_steps+=1
#                       pointsCoordinates = crg.pointsCoordinates(end_point_id, currentConfig)　# 描画には必要だが、ここでは不要
                        fireCount = crg.fireCount(end_point_id, currentConfig)
                        greenCount = crg.greenCount(end_point_id, currentConfig)
                        num_occupied_sites += fireCount
                        updatedConfig = crg.fireSpread(lattice_x, lattice_y, end_point_id, currentConfig)
                        currentConfig = updatedConfig
                clusters_list.append(num_occupied_sites)

        return clusters_list
