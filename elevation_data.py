import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# API_KEY = os.getenv("ELEVATION_API_KEY")

def get_data():
    url = "https://api.airmap.com/elevation/v1/ele/carpet?points=49.9760329253738,14.128741875966284,49.97493584462879,14.130635515530571"
    response = requests.get(url)    
    return response



if __name__ == "__main__":
    response = get_data()
    print(response.json())
