import numpy as np
from flask import Flask
from elevation_data import get_airmap_data, get_sample_airmap_data
from heatmap_generation import compute_heatmap

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/test')
def test():
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    heatmap, best_loc = compute_heatmap(carpet)
    return 'done'