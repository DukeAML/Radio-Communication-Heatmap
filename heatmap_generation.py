from scipy import signal
from scipy import misc
import numpy as np
from elevation_data import get_airmap_data, get_sample_airmap_data
import matplotlib.pyplot as plt
from PIL import Image
import math

def compute_heatmap(elevation_grid, lat1, lng1, lat2, lng2, n = 5): 
    """ Applies a U-shaped kernel (with orientation based on the positions of the soldiers and the party to communicate
        with) to the geographical data and returns a list of the best locations (number of locations specified by 
        the n parameter)

    Parameters
    ----------
    elevation_grid : 2D array
        Geographical data
    lat1 : float/double
        Latitude of the soldier's position
    lng1 : float/double
        Longitude of the soldier's position
    lat2 :float/double
        Latitude of the position with which soldiers want to communicate
    lng2 : float/double
        Longitude of the position with which soldiers want to communicate
    n : int
        Number of "best" locations to return

    Returns
    -------
    corr : 2D array
        Array of values representing the viability of the position to prevent radio signal jamming
    best_loc : nested list
        A nested list of the coordinates of the best points, with each coordinate as a list in the form [y, x]

    """
    
    angle = calculate_bearing_angle(lat1, lng1, lat2, lng2)
    
    sample_filter = np.array([[0, -2, -2, -2, 0],
                              [1, .5, -2, .5, 1],
                              [1, .5, -2, .5, 1],
                              [1,  1, .5,  1, 1],
                              [0,  1,  1,  1, 0]])
    
    rotated_filter = rotate_filter(sample_filter, angle)
    
    corr = signal.correlate2d(elevation_grid, rotated_filter, boundary='symm', mode='valid')          
    best_loc = find_best_locations(corr, n)
    return corr, best_loc


def rotate_filter(filter, degrees):
    """ Rotates a 2D array by an angle of degrees, using bilinear interpolation
    
    Parameters
    ----------
    filter : 2D numpy array
        Can be any shape, but must be a 2D numpy array.
    degrees : float/double/int
        How many degrees to rotate the array.

    Returns
    -------
    rotated_filter : 2D array
        2D array that is rotated relative to the input by an angle of degrees.
        
    """
    
    img = Image.fromarray(filter)
    rotated_img = img.rotate(degrees, resample=Image.BILINEAR)
    rotated_filter = np.asarray(rotated_img)

    return rotated_filter


def calculate_bearing_angle(lat1, lng1, lat2, lng2):
    """ Calculates the angle in degrees clockwise from north between the first
    and second point
    
    https://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
    https://stackoverflow.com/questions/3932502/calculate-angle-between-two-latitude-longitude-points

    Parameters
    ----------
    lat1 : float/double
        Latitude of first point, in degrees.
    lng1 : float/double
        Longitude of first point, in degrees.
    lat2 : float/double
        Latitude of second point, in degrees.
    lng2 : float/double
        Longitude of second point, in degrees.

    Returns
    -------
    brng : float, angle in degrees
        Angle in degrees between the first point and the second point measured
        clockwise from North.

    """
    
    lat1, lng1, lat2, lng2 = math.radians(lat1), math.radians(lng1), math.radians(lat2), math.radians(lng2)
    delta_lng = lng2-lng1

    y = math.cos(lat2) * math.sin(delta_lng)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lng)

    brng = math.atan2(y, x)

    brng = math.degrees(brng)
    brng = (brng + 360) % 360
    return brng


def find_best_locations(corr, n = 5, radius = 2):
    """ Find up to the n-th best locations based on the correlated 2D array (corr)

    Parameters
    ----------
    corr: 2D array
        Array of values representing the viability of the position to prevent radio signal jamming
    n: int
        Number of "best" locations to return
    
    Returns
    -------
    best_loc: nested list
        A nested list of the coordinates of the best points, with each coordinate as a list in the form [y, x]
        
    """

    max_indices = corr.ravel().argsort()[::-1] # sorted in order from maximum to minimum
    best_loc = [list(np.unravel_index(max_indices[0], corr.shape))]
    occupied_ycoor = [*range(best_loc[0][0]-radius, best_loc[0][0]+(radius+1))]
    occupied_xcoor = [*range(best_loc[0][1]-radius, best_loc[0][1]+(radius+1))]

    for i in max_indices[1:]:
        coordinate = list(np.unravel_index(i, corr.shape))
        if len(best_loc) == n:
            break
        if (coordinate[0] in occupied_ycoor) and (coordinate[1] in occupied_xcoor):
            pass
        else:
            if len(best_loc) < n:
                best_loc.append(coordinate)
                occupied_ycoor += [*range(coordinate[0]-radius, coordinate[0]+(radius+1))]
                occupied_xcoor += [*range(coordinate[1]-radius, coordinate[1]+(radius+1))]

    return best_loc

    
if __name__ == "__main__":

    # Test to make sure calculate_bearing_angle works
    print(calculate_bearing_angle(39.099912, -94.581213, 38.627089, -90.200203)) # Should return 96.51
    print(calculate_bearing_angle(8.46696, -17.03663, 65.35996, -17.03663)) # Should return 0 degrees
    
    # Test to make sure compute_heatmap works
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    # print(carpet)
    heatmap, best_loc = compute_heatmap(carpet, 39.099912, -94.581213, 38.627089, -90.200203)
    print(best_loc)

    plt.figure(1)
    plt.title("Elevation Grid")
    plt.imshow(carpet)

    plt.figure(2)
    plt.title("Heatmap")
    for i in range(len(best_loc)):
        plt.plot(best_loc[i][1], best_loc[i][0], 'ro')
    plt.imshow(heatmap)

    # Test to make sure rotate_filter works
    sample_filter = np.array([[0, -2, -2, -2, 0],
                              [1, .5, -2, .5, 1],
                              [1, .5, -2, .5, 1],
                              [1,  1, .5,  1, 1],
                              [0,  1,  1,  1, 0]])

    plt.figure(3)
    plt.imshow(sample_filter)
    plt.title("Sample Filter")

    plt.figure(4)
    plt.imshow(rotate_filter(sample_filter, 45))
    plt.title("Rotated Filter")
    plt.show()