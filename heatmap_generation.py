from scipy import signal
from scipy import misc
import numpy as np
from elevation_data import get_airmap_data, get_sample_airmap_data
import matplotlib.pyplot as plt


def compute_heatmap(elevation_grid):

    # Need to pick kernels
    sample_filter = [[0, -2, -2, -2, 0],
                     [1, .5, -2, .5, 1],
                     [1, .5, -2, .5, 1],
                     [1,  1, .5,  1, 1],
                     [0,  1,  1,  1, 0]]
    
    corr = signal.correlate2d(elevation_grid, sample_filter, boundary='symm', mode='valid')          
    best_loc = np.unravel_index(np.argmax(corr), corr.shape)
    return corr, best_loc



if __name__ == "__main__":
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    heatmap, best_loc = compute_heatmap(carpet)
    plt.figure(1)
    plt.title("Elevation Grid")
    plt.imshow(carpet)

    plt.figure(2)
    plt.title("Heatmap")
    plt.plot(best_loc[1], best_loc[0], 'ro')
    plt.imshow(heatmap)
    plt.show()
    