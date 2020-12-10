from scipy import signal
from scipy import misc
import numpy as np
from elevation_data import *
import matplotlib.pyplot as plt


def compute_heatmap(elevation_grid):
    
    sample_filter = [[0, -2, -2, -2, 0],
                     [1, .5, -2, .5, 1],
                     [1, .5, -2, .5, 1],
                     [1,  1, .5,  1, 1],
                     [0,  1,  1,  1, 0]]
    
    corr = signal.correlate2d(elevation_grid, sample_filter, boundary='symm', mode='valid')          
    
    return corr



if __name__ == "__main__":
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    heatmap = compute_heatmap(carpet)
    plt.figure(1)
    plt.imshow(carpet)
    plt.figure(2)
    plt.imshow(heatmap)
    