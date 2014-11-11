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
center_damping = 0.01
vel_matching_strength = 0.125

# initialisation
boids_x = np.array([random.uniform(-450, 50.0) for x in range(num_boids)])
boids_y = np.array([random.uniform(300.0, 600.0) for x in range(num_boids)])
boid_x_velocities = np.array([random.uniform(0, 10.0) for x in range(num_boids)])
boid_y_velocities = np.array([random.uniform(-20.0, 20.0) for x in range(num_boids)])
boids = (boids_x, boids_y, boid_x_velocities, boid_y_velocities)


def fly_towards_centre(xs, ys, xvs, yvs, center_damping):
    """Boids fly towards the center of all other boids."""
    for i in range(len(xs)):
        for j in range(len(xs)):
            xvs[i] = xvs[i] + (xs[j] - xs[i]) * center_damping / len(xs)
            yvs[i] = yvs[i] + (ys[j] - ys[i]) * center_damping / len(xs)


def avoid_nearby_boids(xs, ys, xvs, yvs, neighbor_dist_cutoff):
    """Keep some distance to nearby boids."""
    for i in range(len(xs)):
        for j in range(len(xs)):
            if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < neighbor_dist_cutoff:
                xvs[i] = xvs[i] + (xs[i] - xs[j])
                yvs[i] = yvs[i] + (ys[i] - ys[j])


def adapt_speed(xs, ys, xvs, yvs, neighbor_vel_dist_cutoff):
    """Try to match speed with nearby boids"""
    for i in range(len(xs)):
        for j in range(len(xs)):
            if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < neighbor_vel_dist_cutoff:
                xvs[i] = xvs[i] + (xvs[j] - xvs[i]) * vel_matching_strength / len(xs)
                yvs[i] = yvs[i] + (yvs[j] - yvs[i]) * vel_matching_strength / len(xs)


def update_boids(boids):
    xs, ys, xvs, yvs = boids
    fly_towards_centre(xs, ys, xvs, yvs, center_damping)
    avoid_nearby_boids(xs, ys, xvs, yvs, neighbor_dist_cutoff)
    adapt_speed(xs, ys, xvs, yvs, neighbor_vel_dist_cutoff)

    for i in range(len(xs)):
        xs[i] = xs[i] + xvs[i]
        ys[i] = ys[i] + yvs[i]


figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids[0], boids[1])

def animate(frame):
    update_boids(boids)
    scatter.set_offsets(zip(boids[0], boids[1]))


anim = animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
