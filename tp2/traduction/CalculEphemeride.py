#--------------------------------------------------------------------------
# Fonction pour calculer les coordonnées des satellites à partir des
# éphémérides en fonction du temps GPS qui correspond à l'instant de départ
# du signal
#
#--------------------------------------------------------------------------

from numpy import sin, cos, arctan2
def CalculEphemeride(t_GPS,Ephem):

    #Pi = 3.1415926535898  % on définit Pi avec le bon nombre de décimales

    mu = 398600500000000              # Constante liée à la gravitation de la Terre
    omegadote = 7.2921151467E-5  # Constante vitesse de rotation de la terre

    _, toe, ecc, i0, omega0, omega, M0, idot, omegadot, deltan, cuc, cus, crc, crs, cic, cis, sqrt_a, _, _, _, _, _ = Ephem
    a = sqrt_a ** 2
    """
    toe = Ephem(2)               # Temps GPS à partir duquel les éphémérides sont valables
    ecc = Ephem(3)               # Excentricité de la trajectoire
    i0 = Ephem(4)                # Inclinaison à l'instant toe
    omega0 = Ephem(5)            # Longitude du noeud ascendant
    omega = Ephem(6)             # Argument du périgée à l'instant toe
    M0 = Ephem(7)                # Anomalie moyenne
    idot = Ephem(8)              # Taux de variation de l'inclinaison 
    omegadot = Ephem(9)          # Taux de variation de la longitude du noeud ascendant  
    deltan = Ephem(10)           # Correction du mouvement moyen
    cuc = Ephem(11)              # Amplitude du cosinus de correction à l'argument de la latitude
    cus = Ephem(12)              # Amplitude du sinus de correction à l'argument de la latitude
    crc = Ephem(13)              # Amplitude du cosinus de correction du rayon orbital
    crs = Ephem(14)              # Amplitude du sinus de correction du rayon orbital
    cic = Ephem(15)              # Amplitude du cosinus de correction de l'inclinaison
    cis = Ephem(16)              # Amplitude du sinus de correction de l'inclinaison
    a = Ephem(17) ** 2              # Demi grand axe
    """

    # Calcul de la position des satellites

    n0 = (mu / a ** 3) ** 0.5

    N = n0 + deltan

    # Mise à jour du temps

    tk = t_GPS - toe

    if tk > 302400:        #procédure pour les problèmes de transition d'une semaine à l'autre
        tk = tk - 604800
    elif tk < -302400:
        tk = tk + 604800


    # Calcul de l'anomalie excentrique 

    Mk = M0 + N * tk
    Ek = Mk
    #op = abs(Mk - Ek + ecc * sin(Ek))

    while abs(Mk - Ek + ecc * sin(Ek)) > 10 ** -12:   #boucle de calcul de Ek

        Ek = Ek - (Ek - ecc * sin(Ek) - Mk) / (1 - ecc * cos(Ek))
        #op = abs(Mk - Ek + ecc * sin(Ek))


    # Applicationdes corrections orbitales

    sinusVk = (sin(Ek) * (1 - ecc ** 2) ** 0.5) / (1 - ecc * cos(Ek))

    cosinusVk = (cos(Ek) - ecc) / (1 - ecc * cos(Ek))
                                                                                                                                                 
    Phik = arctan2(sinusVk, cosinusVk) + omega

    deltaPhik = cus * sin(2 * Phik) + cuc * cos(2 * Phik)
    deltark = crs * sin(2 * Phik) + crc * cos(2 * Phik)
    deltaik = cis * sin(2 * Phik) + cic * cos(2 * Phik)

    uk = Phik + deltaPhik
    rk = a * (1 - ecc * cos(Ek)) + deltark
    ik = i0 + idot * tk + deltaik
    Omegak = omega0 + (omegadot - omegadote) * tk - omegadote * toe
    xp = rk * cos(uk)
    yp = rk * sin(uk)

    Xs = xp * cos(Omegak) - yp * cos(ik) * sin(Omegak)
    Ys = xp * sin(Omegak) + yp * cos(ik) * cos(Omegak)
    Zs = yp * sin(ik)

    return [Xs, Ys, Zs]
