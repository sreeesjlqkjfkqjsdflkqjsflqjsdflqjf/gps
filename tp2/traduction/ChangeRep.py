
# -------------------------------------------------------------------------
# 
#   Fonction pour changer de repère en centrant sur un point
#   (x,y,z) devient (y,z,x)
# 
# -------------------------------------------------------------------------
from math import pi, sin, cos
import numpy as np
def ChangeRep(X,Y,Z,Xcent,Ycent,Zcent,long,lat):

    # on crée les deux matrices inverses de rotation

    pinv1 = np.array([[cos(long*pi/180),sin(long*pi/180),0], [-1*sin(long*pi/180),cos(long*pi/180),0], [0,0,1]])
    pinv2 = np.array([[cos(lat*pi/180),0,sin(lat*pi/180)],  [0,1,0], [ -1*sin(lat*pi/180),0,cos(lat*pi/180)]])

    # on applique les rotations au point central désiré

    PtCentral = pinv1@pinv2@np.array([[Xcent], [Ycent], [Zcent]])

    # on applique les rotations au point lui-même et la translation

    Ptnr = pinv1@pinv@np.array([[X], [Y], [Z]]) - PtCentral

    # on met les points
    return Ptnr

    Xnrep = Ptnr[1]
    Ynrep = Ptnr[2]
    Znrep = Ptnr[3]

    return [Xnrep, Ynrep, Znrep]
