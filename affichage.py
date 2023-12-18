import matplotlib.pyplot as plt
from math import sqrt, cos, sin, acos
import numpy as np
ALT_SAT = 20200/6400
ALT_REC = 1.3
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






def placepoint(point, ax, c='Blue', marker="P"):
    """place un point(np.array(3)) dans le graphique 3d"""
    ax.scatter(point[0], point[1], point[2], c=c, marker = marker, s = 100)

def SatelliteAuPif(rng):
    """renvoie un point aléatoirement placé sur la sphère de rayon ALT_SaT"""
    lam, phi = 2*np.pi*rng.random()-np.pi, 2*np.pi*rng.random()-np.pi
    return ALT_SAT*np.array([cos(phi)*sin(lam), sin(phi)*sin(lam), cos(lam)])


def RecepteurAuPif(rng):
    lam, phi = 2*np.pi*rng.random()-np.pi, 2*np.pi*rng.random()-np.pi
    print(lam, phi)
    return ALT_REC*np.array([cos(phi)*sin(lam), sin(phi)*sin(lam), cos(lam)])


def gentilSatellite(point, elevation):
    lam = acos(point[2]/ALT_REC) 
    phi = acos(point[0]/(sin(lam)*ALT_REC))*(1 if point[1]>=0 else -1)
    print(lam, phi)
    sat1 = ALT_SAT*np.array([cos(phi)*sin(lam-elevation), sin(phi)*sin(lam-elevation), cos(lam-elevation)])
    val_maj = sqrt(2)/2
    sat2 = ALT_SAT*np.array([cos(phi+val_maj*elevation/abs(sin(lam+elevation*val_maj)))*sin(lam+elevation*val_maj), sin(phi+val_maj*elevation/abs(sin(lam+elevation*val_maj)))*sin(lam+elevation*val_maj), cos(lam+elevation*val_maj)])
    sat3 = ALT_SAT*np.array([cos(phi-val_maj*elevation/abs(sin(lam+elevation*val_maj)))*sin(lam+elevation*val_maj), sin(phi-val_maj*elevation/abs(sin(lam+elevation*val_maj)))*sin(lam+elevation*val_maj), cos(lam+elevation*val_maj)])
    return sat1, sat2, sat3
    
def main():
    
    rng = np.random.default_rng()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_aspect("equal")
    ax.set_box_aspect([1,1,1])
    set_axes_equal(ax)
    ax.set_axis_off()
    u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    for _ in range(0):
        placepoint(SatelliteAuPif(rng), ax)

    rec = RecepteurAuPif(rng)
    placepoint(rec, ax, c='r', marker='*')
    for gs in gentilSatellite(rec, 0.4):
        placepoint(gs, ax)
    for gs in gentilSatellite(rec, 0):
        placepoint(gs, ax)
    for gs in gentilSatellite(rec, 0.3):
        placepoint(gs, ax)
    for gs in gentilSatellite(rec, 0.5):
        placepoint(gs, ax)
    plt.show()



if __name__ == "__main__": 
    main()
