"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

import random
from numpy import array

# Will now add an Eagle to Boids

class Boid(object):
    def __init__(self, x, y, xv, yv, owner):
        self.position = array([x, y])
        self.velocity = array([xv, yv])
        self.owner = owner


class Starling(Boid):
    def __init__(self, x, y, xv, yv, owner):
        super(Starling, self).__init__(x, y, xv, yv, owner)

    def interaction(self, other):
        delta_v = array([0.0, 0.0])
        separation = other.position - self.position
        separation_sq = separation.dot(separation)

        if isinstance(other, Eagle):
            # Flee the Eagle
            if separation_sq < self.owner.eagle_avoidance_radius**2:
                delta_v -= (separation * self.owner.eagle_fear) / separation.dot(separation)
                return delta_v

        # Fly towards the middle
        delta_v += separation * self.owner.flock_attraction

        # Fly away from nearby Starlings
        if separation_sq < self.owner.avoidance_radius**2:
            delta_v -= separation

        # Try to match speed with nearby Starlings
        if separation_sq < self.owner.formation_flying_radius**2:
            delta_v += (other.velocity - self.velocity) * self.owner.speed_matching_strength

        return delta_v


class Eagle(Boid):
    def __init__(self, x, y, xv, yv, owner):
        super(Eagle, self).__init__(x, y, xv, yv, owner)

    def interaction(self, other):
        delta_v = array([0.0, 0.0])
        separation = other.position - self.position
        separation_sq = separation.dot(separation)

        if isinstance(other, Eagle):
            # Avoid the other Eagle(s)
            if separation_sq < self.owner.eagle_avoidance_radius**2:
                delta_v -= (separation * self.owner.eagle_fear) / separation.dot(separation)
                return delta_v

        # Hunt the boids
        delta_v += separation * self.owner.eagle_hunt_strength

        return delta_v


# Deliberately terrible code for teaching purposes
class Boids(object):
    def __init__(self):
        self.flock_attraction        = None
        self.avoidance_radius        = None
        self.formation_flying_radius = None
        self.speed_matching_strength = None
        self.eagle_avoidance_radius  = 100
        self.eagle_fear              = 5000
        self.eagle_hunt_strength     = 0.00005
        self.boids                   = []

    def update(self):
        for me in self.boids:
            delta_v = array([0.0, 0.0])
            for him in self.boids:
                delta_v += me.interaction(him)
            # Accelerate as stated
            me.velocity += delta_v
            # Move according to velocities
            me.position += me.velocity


class FlockBuilder(object):
    def start_flock_setup(self):
        self.flock = Boids()
        self.flock.boids = []

    def set_flock_attraction(self, flock_attraction):
        self.flock.flock_attraction = flock_attraction

    def set_avoidance_radius(self, avoidance_radius):
        self.flock.avoidance_radius = avoidance_radius

    def set_formation_flying_radius(self, formation_flying_radius):
        self.flock.formation_flying_radius = formation_flying_radius

    def set_speed_matching_strength(self, speed_matching_strength):
        self.flock.speed_matching_strength = speed_matching_strength

    def set_eagle_parameters(self, eagle_avoidance_radius=100, eagle_fear=5000, eagle_hunt_strength=0.00005):
        self.flock.eagle_avoidance_radius = eagle_avoidance_radius
        self.flock.eagle_fear = eagle_fear
        self.flock.eagle_hunt_strength = eagle_hunt_strength

    def add_Starling(self, x, y, xv, yv):
        self.flock.boids.append(Starling(x, y, xv, yv, self.flock))

    def add_Eagle(self, x, y, xv, yv):
        self.flock.boids.append(Eagle(x, y, xv, yv, self.flock))

    def initialise_random(self, count):
        for _ in range(count):
            self.add_Starling(random.uniform(-450, 50.0),
                              random.uniform(300.0, 600.0),
                              random.uniform(0, 10.0),
                              random.uniform(-20., 20.))

    def initialise_from_data(self, data):
        for x, y, xv, yv in zip(*data):
            self.add_Starling(x, y, xv, yv)

    def create_flock(self):
        return self.flock

