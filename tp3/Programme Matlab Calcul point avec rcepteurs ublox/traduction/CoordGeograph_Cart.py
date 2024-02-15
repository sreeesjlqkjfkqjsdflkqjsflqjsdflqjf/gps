import numpy as np

# -------------------------------------------------------------------------
#
#   Fonction pour convertir les coordonn�es g�ographiques (en d�gr�s)
#   en coordonn�es cart�siennes
#
# -------------------------------------------------------------------------


a = 6378137
ec = 0.00669437999014


def CoordGeograph_Cart(lat, long, alt):
    phi = lat * np.pi / 180
    lamb = long * np.pi / 180
    x = a * np.cos(lamb) / (1 + (1 - ec) * np.tan(phi) ** 2) ** .5 + alt * np.cos(lamb) * np.cos(phi)
    y = a * np.sin(lamb) / (1 + (1 - ec) * np.tan(phi) ** 2) ** .5 + alt * np.sin(lamb) * np.cos(phi)
    z = a * (1 - ec) * np.sin(phi) / (1 - ec * np.sin(phi) ** 2) ** .5 + alt * np.sin(phi)
    return np.array((x, y, z))
