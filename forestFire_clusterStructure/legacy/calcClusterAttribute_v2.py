
import numpy as np

def calcClusterAttribute(cluster_coordinates):

#    print(cluster_coordinates)

    s = len(cluster_coordinates) #number of occupied sites in this cluster_str

    x_coordinates = [cluster_coordinates[i][0] for i in range(s)]
    y_coordinates = [cluster_coordinates[i][1] for i in range(s)]
#    cog_x = np.mean(x_coordinates)
#    cog_y = np.mean(y_coordinates)
    var_x = np.var(x_coordinates)
    var_y = np.var(y_coordinates)
    radius_gyration = np.sqrt(var_x + var_y)
    cluster_attribute = [s, radius_gyration]

    return cluster_attribute
