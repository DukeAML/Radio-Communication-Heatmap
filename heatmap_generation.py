from scipy import signal
from scipy import misc
import numpy as np
from elevation_data import get_airmap_data, get_sample_airmap_data
import matplotlib.pyplot as plt
from PIL import Image
import math


def compute_heatmap(elevation_grid):

    sample_filter = np.array([[0, -2, -2, -2, 0],
                              [1, .5, -2, .5, 1],
                              [1, .5, -2, .5, 1],
                              [1,  1, .5,  1, 1],
                              [0,  1,  1,  1, 0]])
    
    corr = signal.correlate2d(elevation_grid, sample_filter, boundary='symm', mode='valid')          
    best_loc = np.unravel_index(np.argmax(corr), corr.shape)

    return corr, best_loc


def rotate_filter(filter, degrees):
    
    img = Image.fromarray(filter)
    rotated_img = img.rotate(degrees)
    rotated_filter = np.asarray(rotated_img)
    
    return rotated_filter

def calculate_bearing_angle(lat1, lng1, lat2, lng2):
    # https://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
    lat1, lng1, lat2, lng2 = math.radians(lat1), math.radians(lng1), math.radians(lat2), math.radians(lng2)
    delta_lng = lng2-lng1

    y = math.cos(lat2) * math.sin(delta_lng)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lng)

    brng = math.atan2(y, x)

    brng = math.degrees(brng)
    brng = (brng + 360) % 360
    return brng

if __name__ == "__main__":
    
    print(calculate_bearing_angle(39.099912, -94.581213, 38.627089, -90.200203)) # Should return 96.51
    
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    print(carpet)
    heatmap, best_loc = compute_heatmap(carpet)
    plt.figure(1)
    plt.title("Elevation Grid")
    plt.imshow(carpet)

    plt.figure(2)
    plt.title("Heatmap")
    plt.plot(best_loc[1], best_loc[0], 'ro')
    plt.imshow(heatmap)

    
    sample_filter = np.array([[0, -2, -2, -2, 0],
                              [1, .5, -2, .5, 1],
                              [1, .5, -2, .5, 1],
                              [1,  1, .5,  1, 1],
                              [0,  1,  1,  1, 0]])

    plt.figure(3)
    plt.imshow(sample_filter)
    plt.title("sample_filter")

    plt.figure(4)
    plt.imshow(rotate_filter(sample_filter, 45))
    plt.title("rotated_filter")
    plt.show()


    