from boids import update_boids, fly_towards_centre, distance, avoid_nearby_boids, match_speed
from nose.tools import assert_almost_equal
import os
import yaml
import numpy as np

def test_bad_boids_regression():
    regression_data = yaml.load(open(os.path.join(os.path.dirname(__file__), 'fixture.yml')))
    boid_data_before = regression_data["before"]
    boid_data_after = regression_data["after"]

    update_boids(boid_data_before)
    for list_after, list_before in zip(boid_data_after, boid_data_before):
        for vec_after, vec_before in zip(list_after, list_before):
            for val_after, val_before in zip(vec_after, vec_before):
                assert_almost_equal(val_after, val_before, delta=0.01)


def test_fly_towards_centre():
    boids_pos = [np.array([2,0]), np.array([10,1]), np.array([0,1]), np.array([0,3])]
    boids_vel = [np.array([-1,1]), np.array([0,1]), np.array([1,1]), np.array([0,1])]
    attraction_const = 0.01
    boids_vel = fly_towards_centre(boids_pos, boids_vel, attraction_const)

    boids_vel_after = [np.array([-0.99, 1.0125]), np.array([-0.07, 1.0025]), np.array([1.03, 1.0025]), np.array([0.03, 0.9825])]
    for boids, reference in zip(boids_vel, boids_vel_after):
        for boid, ref in zip(boids, reference):
            assert_almost_equal(boid, ref)


def test_distance():
    vec1 = np.array([1,1])
    vec2 = np.array([0,0])
    assert_almost_equal(distance(vec1, vec2), np.sqrt(2))


def test_avoid_nearby_boids():
    boids_pos = [np.array([2,0]), np.array([10,1]), np.array([0,1]), np.array([0,3])]
    boids_vel = [np.array([-1,1]), np.array([0,1]), np.array([1,1]), np.array([0,1])]
    neighbor_dist_cutoff = 100
    boids_vel = avoid_nearby_boids(boids_pos, boids_vel, neighbor_dist_cutoff)

    boids_vel_after = [np.array([-5, -4]), np.array([8, 2]), np.array([-1, 0]), np.array([-2, 6])]
    for boids, reference in zip(boids_vel, boids_vel_after):
        for boid, ref in zip(boids, reference):
            assert_almost_equal(boid, ref)


def test_match_speed():
    boids_pos = [np.array([2,0]), np.array([10,1]), np.array([0,1]), np.array([0,3])]
    boids_vel = [np.array([-10,1]), np.array([0,10]), np.array([1,1]), np.array([10,10])]
    neighbor_vel_dist_cutoff= 10000
    boids_vel = match_speed(boids_pos, boids_vel, neighbor_vel_dist_cutoff)

    boids_vel_after = [np.array([-7, 1]), np.array([0, 8]), np.array([0, 1]), np.array([7, 7])]
    for boids, reference in zip(boids_vel, boids_vel_after):
        for boid, ref in zip(boids, reference):
            assert_almost_equal(boid, ref)


