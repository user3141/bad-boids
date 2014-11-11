"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np


# parameters
num_boids = 50
neighbor_dist_cutoff = 100
neighbor_vel_dist_cutoff = 10000
attraction_const = 0.01
vel_matching_strength = 0.125

# initialisation
boids_pos = [np.array([random.uniform(-450, 50.0), random.uniform(300.0, 600.0)]) for _ in range(num_boids)]
boids_vel = [np.array([random.uniform(   0, 10.0), random.uniform(-20.0,  20.0)]) for _ in range(num_boids)]
boids = (boids_pos, boids_vel)


def fly_towards_centre(boids_pos, boids_vel, attraction_const):
    """Boids fly towards the center of all other boids."""
    new_boids_vel = []
    for boid1_pos, boid_vel in zip(boids_pos, boids_vel):
        for boid2_pos in boids_pos:
            boid_vel = boid_vel + (boid2_pos - boid1_pos) * attraction_const / len(boids_pos)
            #boid_vel += (boid2_pos - boid1_pos) * attraction_const / len(boids_pos)
        new_boids_vel.append(boid_vel)
    boids_vel[0:] = [new_boid_vel for new_boid_vel in new_boids_vel]
    return boids_vel


def distance(vec1, vec2):
    """Distance between two vectors"""
    diff_vec = vec1 - vec2
    return np.sqrt(np.sum(x_i**2 for x_i in diff_vec))


def avoid_nearby_boids(boids_pos, boids_vel, neighbor_dist_cutoff):
    """Keep some distance to nearby boids."""
    new_boids_vel = []
    for boid1_pos, boid_vel in zip(boids_pos, boids_vel):
        for boid2_pos in boids_pos:
            if distance(boid1_pos, boid2_pos) < np.sqrt(neighbor_dist_cutoff):
                boid_vel += (boid1_pos - boid2_pos)

        new_boids_vel.append(boid_vel)
    boids_vel[0:] = [new_boid_vel for new_boid_vel in new_boids_vel]
    return boids_vel


def match_speed(boids_pos, boids_vel, neighbor_vel_dist_cutoff):
    """Try to match speed with nearby boids"""
    new_boids_vel = []
    for boid1_pos, boid1_vel in zip(boids_pos, boids_vel):
        for boid2_pos, boid2_vel in zip(boids_pos, boids_vel):
            if distance(boid1_pos, boid2_pos) < np.sqrt(neighbor_vel_dist_cutoff):
                boid1_vel += (boid2_vel - boid1_vel) * vel_matching_strength / len(boids_pos)

        new_boids_vel.append(boid1_vel)
    boids_vel[0:] = [new_boid_vel for new_boid_vel in new_boids_vel]
    return boids_vel


def update_boids(boids):
    boids_pos, boids_vel = boids
    fly_towards_centre(boids_pos, boids_vel, attraction_const)
    avoid_nearby_boids(boids_pos, boids_vel, neighbor_dist_cutoff)
    match_speed(boids_pos, boids_vel, neighbor_vel_dist_cutoff)

    new_boids_pos = []
    for boid_pos, boid_vel in zip(boids_pos, boids_vel):
        boid_pos = boid_pos + boid_vel
        new_boids_pos.append(boid_pos)
    boids_pos[0:] = [boid_pos for boid_pos in new_boids_pos]

def animate(frame):
    update_boids(boids)
    boids_pos, boids_vel = boids
    x_vals = [x[0] for x in boids_pos]
    y_vals = [x[1] for x in boids_pos]
    scatter.set_offsets(zip(x_vals, y_vals))


figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
x_vals = [x[0] for x in boids_pos]
y_vals = [x[1] for x in boids_pos]
scatter = axes.scatter(x_vals, y_vals)

anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
