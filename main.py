import numpy as np
from flask import Flask
from elevation_data import *
from heatmap_generation import compute_heatmap


'''
What we need to do:

import dted data or other elevation data
generate heatmap - needs to be fleshed out further
provide results to the front end

'''

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'

@app.route('/test')
def test():
    stats, carpet = get_airmap_data(47.6062, 122.3321)
    heatmap = compute_heatmap(carpet)
    return 'done'