import matplotlib.pyplot as plt
import numpy as np

altitudeDuSatellite = 20200/6400

def placepoint(x, y, z, ax):
    ax.scatter(x, y, z, c='Blue', marker = 'P', s = 100)

def SatelliteAuPif(rng):
    lam, phi = *np.pi*rng.random(1, 2)
    return altitudeDuSatellite*np.array([lam*phi, phi, ])



def main():
    
    rng = np.random.default_rng(seed=1337)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_axis_off()
    u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    placepoint(0.5, ax)
    plt.show()



if __name__ == "__main__": 
    main()
