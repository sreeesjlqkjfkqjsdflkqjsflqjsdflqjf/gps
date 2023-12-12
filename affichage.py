import matplotlib.pyplot as plt
from math import cos, sin
import numpy as np
ALT_SAT = 20200/6400

def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 2 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)

def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])





def placepoint(point, ax):
    ax.scatter(point[0], point[1], point[2], c='Blue', marker = 'P', s = 100)

def SatelliteAuPif(rng):
    lam, phi = 2*np.pi*rng.random()+np.pi, 2*np.pi*rng.random()+np.pi
    return ALT_SAT*np.array([cos(phi)*cos(lam), sin(phi)*cos(lam), sin(lam)])



def main():
    
    rng = np.random.default_rng(seed=1337)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_aspect("equal")
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)
    ax.set_axis_off()
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    for _ in range(150):
        placepoint(SatelliteAuPif(rng), ax)
    plt.show()



if __name__ == "__main__": 
    main()
