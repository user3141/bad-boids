"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid = 37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import random
import numpy as np

# Deliberately terrible code for teaching purposes

boids_x           = np.array([random.uniform(-450.,  50.0) for x in range(50)])
boids_y           = np.array([random.uniform( 300., 600.0) for x in range(50)])
boid_x_velocities = np.array([random.uniform(   0.,  10.0) for x in range(50)])
boid_y_velocities = np.array([random.uniform(-20.0,  20.0) for x in range(50)])
boids = [boids_x, boids_y, boid_x_velocities, boid_y_velocities]

def update_boids(boids):
    xs, ys, xvs, yvs = boids

    # Fly towards the middle
    center_x = np.sum(xs) / len(xs)
    center_y = np.sum(ys) / len(ys)
    xvs = xvs + (center_x - xs) * 0.01
    yvs = yvs + (center_y - ys) * 0.01

    # Fly away from nearby boids
    #for i in range(len(xs)):
    #    for j in range(len(xs)):
    #        if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < 100:
    #            xvs[i] = xvs[i] + (xs[i] - xs[j])
    #            yvs[i] = yvs[i] + (ys[i] - ys[j])
    xs_dist_matrix = xs[:, np.newaxis] - xs
    ys_dist_matrix = ys[:, np.newaxis] - ys
    squared_dist_matrix = xs_dist_matrix**2 + ys_dist_matrix**2
    xvs = xvs + np.sum(xs_dist_matrix * (squared_dist_matrix < 100), axis=1)
    yvs = yvs + np.sum(ys_dist_matrix * (squared_dist_matrix < 100), axis=1)

    # Try to match speed with nearby boids
    #for i in range(len(xs)):
    #    for j in range(len(xs)):
    #        if (xs[j] - xs[i])**2 + (ys[j] - ys[i])**2 < 10000:
    #            xvs[i] = xvs[i] + (xvs[j] - xvs[i]) * 0.125 / len(xs)
    #            yvs[i] = yvs[i] + (yvs[j] - yvs[i]) * 0.125 / len(xs)
    xvs_dist_matrix = xvs - xvs[:, np.newaxis]
    yvs_dist_matrix = yvs - yvs[:, np.newaxis]
    xvs = xvs + np.sum(xvs_dist_matrix * (squared_dist_matrix < 10000), axis=1) * 0.125 / len(xs)
    yvs = yvs + np.sum(yvs_dist_matrix * (squared_dist_matrix < 10000), axis=1) * 0.125 / len(xs)

    # Move according to velocities
    for i in range(len(xs)):
        xs[i] = xs[i] + xvs[i]
        ys[i] = ys[i] + yvs[i]

    boids[0] = xs
    boids[1] = ys
    boids[2] = xvs
    boids[3] = yvs

figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids[0], boids[1])

def animate(frame):
   update_boids(boids)
   scatter.set_offsets(zip(boids[0], boids[1]))


anim =  animation.FuncAnimation(figure, animate, frames=50, interval=50)

if __name__ == "__main__":
    #plt.show()
    for i in range(500):
        update_boids(boids)
