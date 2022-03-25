import sys
import glob
import os
import numpy as np
import pdb
import matplotlib.pyplot as plt
import matplotlib.image as img
from scipy import misc
import random

# define a function that does the chamfer algorithm
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

    # chamfer algorithm for both iterations to not have
    # code redundancy
    for n in range(2):
        for i in range(height):
            for j in range(width):
                # special case if in first row and first column
                # no pixels in AL
                if i == 0 and j == 0:
                    continue
                # special case if in first column
                # only one pixel above that is in AL
                elif j == 0:
                    # norm is 1 because the pixel is one above
                    if distance_map[i, j] > (distance_map[i-1, j] + 1):
                        # if the found distance is smaller, update the pixel
                        distance_map[i,j] = (distance_map[i-1, j] + 1)
                # special case if in first row
                # no AL pixels above
                elif i == 0:
                    # look for the smaller values of the two AL pixels
                    minimum = min(distance_map[i, j-1] + 1, distance_map[i+1, j-1] + 2)
                    # if the minimum is smaller, update the distance map
                    if distance_map[i, j] > minimum:
                        distance_map[i, j] = minimum
                # special case if in the last row
                # only three AL pixels
                elif i == height - 1:
                    minimum = min(distance_map[i, j-1] + 1, distance_map[i-1, j-1] + 2, distance_map[i-1, j] + 1)
                    # if the minimum is smaller, update the distance map
                    if distance_map[i, j] > minimum:
                        distance_map[i, j] = minimum
                # all "normal" cases in the picture
                else:
                    minimum = min(distance_map[i+1, j - 1] + 1, distance_map[i, j - 1] + 1,
                                  distance_map[i - 1, j - 1] + 2, distance_map[i - 1, j] + 1)
                    # if the minimum is smaller, update the distance map
                    if distance_map[i, j] > minimum:
                        distance_map[i, j] = minimum

        # after the first iteration, flip the picture
        # then it will do the distancing again on the flipped image
        # after the second iteration it will flip it back such that
        # the original picture is displayed
        distance_map = np.flipud(distance_map)
        distance_map = np.fliplr(distance_map)
        #plt.imshow(distance_map)

    return distance_map


# load shapes
shapes = glob.glob(os.path.join('shapes', '*.png'))

# Chamfer algorithm on each image
for i, shape in enumerate(shapes):
    # load the edge map
    edge_map = img.imread(shape)

    distance_map = chamfer_algorithm(edge_map)

    # the top row of the plots should be the edge maps, and on the bottom the corresponding distance maps
    # place them in the right spot of the grid
    # the edge map starts at 1, which is i+1
    # the distance map starts 4 places later at 5, which is i+5
    k, l = i+1, i+5
    plt.subplot(2, len(shapes), k)
    plt.imshow(edge_map, cmap='gray')
    plt.subplot(2, len(shapes), l)
    plt.imshow(distance_map, cmap='gray')

plt.show()
