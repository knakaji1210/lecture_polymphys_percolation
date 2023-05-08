# Functions necessary to calculate forest fire

import random as rd

def initialConfig(lattice_x, lattice_y, p):

# function for initial tree configuration

    num_black = 0
    num_green = 0
    point_id = 0
    initConfig = []
    point_status = [0,1,2] # 0: soil, 1: green, 2: fire

    for i in range(int(lattice_x)):
        for j in range(int(lattice_y)):
            x = i - (lattice_x / 2 - 0.5)
            y = j - (lattice_y / 2 - 0.5)
            point_coordinate = [x, y]
            if rd.random() > p:
                point_attribute = [point_id, point_status[0], point_coordinate]
                point_id+=1
                num_black+=1
            else:
                point_attribute = [point_id, point_status[1], point_coordinate]
                point_id+=1
                num_green+=1
            initConfig.append(point_attribute)
    return initConfig

def initialFire(lattice_y, currentConfig):

# function for initial firing points

    for i in range(lattice_y):
        point_attribute = currentConfig[i]
        point_status = point_attribute[1]
        if point_status == 1:
            point_attribute[1] = 2
    return currentConfig


def fireSpread(lattice_x, lattice_y, end_point_id, currentConfig):

# function for fire spreading

    for i in range(end_point_id):
        point_attribute = currentConfig[i]
        point_id = point_attribute[0]
        point_status = point_attribute[1]
        if point_id % lattice_y == lattice_y - 1: #ポイントが北一列の場合
            if point_status == 2:
                if point_id == end_point_id - 1 and point_status == 2:
                    point_attribute[1] = 0
                else:
                    pointL_attribute = currentConfig[i + lattice_y]
                    pointL_status = pointL_attribute[1]
                    if pointL_status == 1:
                        pointL_attribute[1] = -1
                    point_attribute[1] = 0
        elif  (lattice_x - 1)*lattice_y - 1 < point_id: #ポイントが東一列の場合
            if point_status == 2:
                point_attribute[1] = 0
        else:
            if point_status == 2:
                pointU_attribute = currentConfig[i+1]
                pointU_status = pointU_attribute[1]
                pointL_attribute = currentConfig[i + lattice_y]
                pointL_status = pointL_attribute[1]
                if pointU_status == 1:
                    pointU_attribute[1] = -1
                if pointL_status == 1:
                    pointL_attribute[1] = -1
                point_attribute[1] = 0
    for j in range(end_point_id):
        point_attribute = currentConfig[j]
        point_status = point_attribute[1]
        if point_status == -1:
            point_attribute[1] = 2
    return currentConfig

def fireCount(end_point_id, currentConfig):

# function for fire spreading

    fireCount = 0

    for i in range(end_point_id):
        point_attribute = currentConfig[i]
        point_status = point_attribute[1]
        if point_status == 2:
            fireCount+=1
    return fireCount

def pointsCoordinates(end_point_id, currentConfig):

    x_black = []
    y_black = []
    x_green = []
    y_green = []
    x_red = []
    y_red = []

    for i in range(end_point_id):
        point_attribute = currentConfig[i]
        if point_attribute[1] == 0:
            point_coordinate = point_attribute[2]
            x = point_coordinate[0]
            y = point_coordinate[1]
            x_black.append(x) 
            y_black.append(y)
        elif point_attribute[1] == 1:
            point_coordinate = point_attribute[2]
            x = point_coordinate[0]
            y = point_coordinate[1]
            x_green.append(x) 
            y_green.append(y)
        elif point_attribute[1] == 2:
            point_coordinate = point_attribute[2]
            x = point_coordinate[0]
            y = point_coordinate[1]
            x_red.append(x) 
            y_red.append(y)

    pointsCoordinates = [x_black, y_black, x_green, y_green, x_red, y_red]

    return pointsCoordinates
