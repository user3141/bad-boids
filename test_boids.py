import boids as bd
from nose.tools import assert_almost_equal,  assert_greater
from nose.tools import assert_less,  assert_equal,  assert_sequence_equal
from numpy.testing import assert_array_equal
import os
import yaml

def test_bad_boids_regriession():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(0.01 / 50)
    flock_builder.set_avoidance_radius(10)
    flock_builder.set_formation_flying_radius(100)
    flock_builder.set_speed_matching_strength(0.125 / 50)
    regression_data = yaml.load(open(os.path.join(os.path.dirname(__file__), 'fixture.yml')))
    flock_builder.initialise_from_data(regression_data["before"])
    boids = flock_builder.create_flock()
    boids.update()
    for index, boid in enumerate(boids.boids):
        assert_almost_equal(boid.position[0], regression_data["after"][0][index], delta=0.01)
        assert_almost_equal(boid.position[1], regression_data["after"][1][index], delta=0.01)
        assert_almost_equal(boid.velocity[0], regression_data["after"][2][index], delta=0.01)
        assert_almost_equal(boid.velocity[1], regression_data["after"][3][index], delta=0.01)


def test_bad_boids_initialisation():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(1.0)
    flock_builder.set_avoidance_radius(10.)
    flock_builder.set_formation_flying_radius(100)
    flock_builder.set_speed_matching_strength(0.5)
    flock_builder.initialise_random(15)
    boids = flock_builder.create_flock()
    assert_equal(len(boids.boids), 15)
    for boid in boids.boids:
        assert_less(boid.position[0], 50.0)
        assert_greater(boid.position[0], -450)
        assert_less(boid.position[1], 600)
        assert_greater(boid.position[1], 300)
        assert_less(boid.velocity[0], 10.0)
        assert_greater(boid.velocity[0], 0)
        assert_less(boid.velocity[1], 20.0)
        assert_greater(boid.velocity[1], -20.0)


def test_boid_interaction_fly_to_middle():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(3.0)
    flock_builder.set_avoidance_radius(2.)
    flock_builder.set_formation_flying_radius(10.)
    flock_builder.set_speed_matching_strength(0.)
    flock_builder.add_Starling(0, 0, 1, 0)
    flock_builder.add_Starling(0, 5, 0, 0)
    boids = flock_builder.create_flock()
    first = boids.boids[0]
    second = boids.boids[1]
    assert_array_equal(first.interaction(second), [0.0, 15.0])

def test_boid_interaction_avoidance():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(3.0)
    flock_builder.set_avoidance_radius(10.)
    flock_builder.set_formation_flying_radius(10.)
    flock_builder.set_speed_matching_strength(0.)
    flock_builder.add_Starling(0, 0, 1, 0)
    flock_builder.add_Starling(0, 5, 0, 0)
    boids = flock_builder.create_flock()
    first = boids.boids[0]
    second = boids.boids[1]
    assert_array_equal(first.interaction(second), [0.0, 10.0])


def test_boid_interaction_formation():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(3.0)
    flock_builder.set_avoidance_radius(2.)
    flock_builder.set_formation_flying_radius(10.)
    flock_builder.set_speed_matching_strength(7.)
    flock_builder.add_Starling(0, 0,  0, 0)
    flock_builder.add_Starling(0, 5, 11, 0)
    boids = flock_builder.create_flock()
    first = boids.boids[0]
    second = boids.boids[1]
    assert_array_equal(first.interaction(second), [11.0 * 7.0, 15.0])


def test_starling_flees_the_eagle():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(3.0)
    flock_builder.set_avoidance_radius(2.)
    flock_builder.set_formation_flying_radius(10.)
    flock_builder.set_speed_matching_strength(7.)
    flock_builder.add_Starling(0, 0, 0, 0)
    flock_builder.add_Eagle(0, 5, 0, 0)
    boids = flock_builder.create_flock()
    first = boids.boids[0]
    second = boids.boids[1]
    assert_array_equal(first.interaction(second), [0.0, -5. * 5000 / 5**2])


def test_eagle_hunts_startling():
    flock_builder = bd.FlockBuilder()
    flock_builder.start_flock_setup()
    flock_builder.set_flock_attraction(3.0)
    flock_builder.set_avoidance_radius(2.)
    flock_builder.set_formation_flying_radius(10.)
    flock_builder.set_speed_matching_strength(7.)
    flock_builder.add_Eagle(0, 0, 0, 0)
    flock_builder.add_Starling(0, 5, 0, 0)
    boids = flock_builder.create_flock()
    first = boids.boids[0]
    second = boids.boids[1]
    assert_array_equal(first.interaction(second), [0.0, 5. * boids.eagle_hunt_strength])

