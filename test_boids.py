from boids import update_boids, fly_towards_centre
from nose.tools import assert_almost_equal
import os
import yaml
import numpy as np

def test_bad_boids_regression():

    def convert_data(boid_data):
        x, y, velx, vely = boid_data
        boids_pos = [np.array([x_i, y_i]) for x_i, y_i in zip(x, y)]
        boids_vel = [np.array([x_i, y_i]) for x_i, y_i in zip(velx, vely)]
        boid_data = (boids_pos, boids_vel)
        return boid_data

    regression_data = yaml.load(open(os.path.join(os.path.dirname(__file__), 'fixture.yml')))
    boid_data_before = convert_data(regression_data["before"])
    boid_data_after = convert_data(regression_data["after"])

    update_boids(boid_data_before)
    for list_after, list_before in zip(boid_data_after, boid_data_before):
        for vec_after, vec_before in zip(list_after, list_before):
            for val_after, val_before in zip(vec_after, vec_before):
                assert_almost_equal(val_after, val_before, delta=0.01)

