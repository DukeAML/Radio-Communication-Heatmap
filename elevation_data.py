import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# API_KEY = os.getenv("ELEVATION_API_KEY")


def get_sample_airmap_data():
    url = "https://api.airmap.com/elevation/v1/ele/carpet?points=49.9960329253738,14.128741875966284,49.97503584462879,14.145005515530571"
    response = requests.get(url)
    response = response.json()
    print(response)
    stats = response['data']['stats']
    carpet = response['data']['carpet']
    return stats, carpet


def get_airmap_data(lat, lng):
    url = "https://api.airmap.com/elevation/v1/ele/carpet?points={},{},{},{}".format(lat+0.01, lng+0.01, lat-0.01, lng-0.01)
    response = requests.get(url)
    response = response.json()
    print(response)
    stats = response['data']['stats']
    carpet = response['data']['carpet']
    return stats, carpet


if __name__ == "__main__":
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    plt.imshow(carpet)


