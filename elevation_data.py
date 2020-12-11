import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# API_KEY = os.getenv("ELEVATION_API_KEY")


def get_sample_airmap_data():
    """ Gets a grid of elevation data centered at a predefined point

    Returns
    -------
    stats : indexable object in format {'max':649, 'min':453, 'avg':536.7581735159818}
        Contains the maximum, minimum and average elevations in the region.
    carpet : 2D array of integers
        Represents the elevation values between the two predefined points, 
        with a spatial resolution of 1 arc second.
        
    """

    url = "https://api.airmap.com/elevation/v1/ele/carpet?points=49.9960329253738,14.128741875966284,49.97503584462879,14.145005515530571"
    response = requests.get(url)
    response = response.json()
    stats = response['data']['stats']
    carpet = response['data']['carpet']
    return stats, carpet



def get_airmap_data(lat, lng):
    """ Gets a grid of elevation data centered around a target point 
    
    Parameters
    ----------
    lat : 
        Latitude of the target point. Limited to between 56 degrees South 
        and 60 degrees North.
    lng : 
        Longitude of the target point.

    Returns
    -------
    stats : indexable object in format {'max':649, 'min':453, 'avg':536.7581735159818}
        Contains the maximum, minimum and average elevations in the region.
    carpet : 2D array of integers
        Represents the elevation values in a square around the specified point 
        with a spatial resolution of 1 arc second.
        
    """
    
    url = "https://api.airmap.com/elevation/v1/ele/carpet?points={},{},{},{}".format(lat+0.01, lng+0.01, lat-0.01, lng-0.01)
    response = requests.get(url)
    response = response.json()
    stats = response['data']['stats']
    carpet = response['data']['carpet']
    return stats, carpet


if __name__ == "__main__":
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    plt.imshow(carpet)


