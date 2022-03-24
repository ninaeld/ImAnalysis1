import sys
import glob
import os
import numpy as np
import pdb
import matplotlib.pyplot as plt
import matplotlib.image as img
from scipy import misc
import random

#define a function that does the chamfer algorithm
def chamfer_algorithm(edge_map):
    height, width = edge_map.shape
    # distance_map: array_like, same size as edge_map
    distance_map = np.zeros((height, width), dtype=float)

    # set all values that are not edges to infinity in the distance map
    for i in range(height):
        for j in range(width):
            # if the value is smaller than 1, it isn't an edge
            if edge_map[i, j] < 1:
                distance_map[i, j] = float('inf')
            # if the value is 1, it is an edge
            elif edge_map[i, j] == 1:
                distance_map[i, j] = 0
            else:
                raise ValueError("Invalid value in original picture")

    # chamfer algorithm first iteration
    for i in range(height):
        for j in range(width):
            # special case if in first row and first column
            if i == 0 and j == 0:
                pass
            # special case if in last row and first column
            elif i == height - 1 and j == 0:
                pass
            # special case if in first row
            elif i == 0:
                pass
            # special case if in first column
            elif j == 0:
                pass
            # special case if in the last row
            elif i == height - 1:
                pass
            # all "normal" cases in the picture
            else:
                pass

    # chamfer algorithm backwards
    # reverse the distance map, so it can be looped through normally
    np.flipud(distance_map)
    np.fliplr(distance_map)
    for i in range(height):
        for j in range(width):
            pass

    return distance_map

# load shapes
shapes = glob.glob(os.path.join('shapes', '*.png'))

#Chamfer algorithm on each image
for i, shape in enumerate(shapes):
    # load the edge map
    edge_map = img.imread(shape)

    chamfer_algorithm(edge_map)


    # the top row of the plots should be the edge maps, and on the bottom the corresponding distance maps
    """k, l = None, None
    plt.subplot(2, len(shapes), k)
    plt.imshow(edge_map, cmap='gray')
    plt.subplot(2, len(shapes), l)"""
    #plt.imshow(distance_map, cmap='gray')
    break

plt.show()
