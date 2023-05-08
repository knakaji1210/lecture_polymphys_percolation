# forest fire statistics

import forestFunc_v2 as ff

def fireExtinctionTime(lattice_x, lattice_y, p):

        end_point_id = lattice_x * lattice_y

        num_repeat = 0

# Building of initial configuration

        initialConfig = ff.initialConfig(lattice_x, lattice_y, p)
        currentConfig = ff.initialFire(lattice_y, initialConfig)
        fireCount = ff.fireCount(end_point_id, currentConfig)

# Stepwise fire spreading

        while fireCount > 0:
                num_repeat+=1
                pointsCoordinates = ff.pointsCoordinates(end_point_id, currentConfig)
                fireCount = ff.fireCount(end_point_id, currentConfig)
                updatedConfig = ff.fireSpread(lattice_x, lattice_y, end_point_id, currentConfig)
                currentConfig = updatedConfig

#        print(num_repeat)
        return num_repeat

def drawStepEvolutionFunc(maxPoints, x_orig_list, y_orig_list):

    x_list = []
    y_list = []

    for i in range(maxPoints):
        x_list.append(x_orig_list[:i+1])
        y_list.append(y_orig_list[:i+1])

    return x_list, y_list