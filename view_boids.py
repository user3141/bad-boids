import boids
from boids import Boids, Eagle
from matplotlib import pyplot as plt
from matplotlib import animation

flock_builder = boids.FlockBuilder()
flock_builder.start_flock_setup()
flock_builder.set_flock_attraction(0.01/50)
flock_builder.set_avoidance_radius(10.)
flock_builder.set_formation_flying_radius(100)
flock_builder.set_speed_matching_strength(0.125/50)
flock_builder.initialise_random(50)
flock_builder.add_Eagle(0, 0, 0, 50)
boids = flock_builder.create_flock()

#boids = Boids(flock_attraction = 0.01/50,
#              avoidance_radius = 10,
#              formation_flying_radius = 100,
#              speed_matching_strength = 0.125/50)

#boids.initialise_random(50)
#boids.add_eagle(0, 0, 0, 50)

figure = plt.figure()
axes = plt.axes(xlim=(-2000, 1500), ylim=(-500, 4000))
scatter = axes.scatter([b.position[0] for b in boids.boids], [b.position[1] for b in boids.boids])

def color(boid):
	if isinstance(boid, Eagle):
		return (1, 0, 0)
	return (0, 0, 1)

def animate(frame):
    boids.update()
    scatter.set_offsets([b.position for b in boids.boids])
    scatter.set_color([color(b) for b in boids.boids])


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()

