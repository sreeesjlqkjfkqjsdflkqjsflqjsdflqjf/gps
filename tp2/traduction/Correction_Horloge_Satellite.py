#--------------------------------------------------------------------------
# Fonction pour calculer les corrections d'horloge satellite et les erreurs
# relativiste en fonction de l'instant de référence GPS
# #
#--------------------------------------------------------------------------
from math import sin, cos

def Correction_Horloge_Satellite(t, Ephem, indice_satelite):

    F = -4.442807633e-10   # Constantes qui dépendent de la gravité terrestre
    mu = 3.986005e14
    a = Ephem[indice_satelite, 16] ** 2
    ecc = Ephem[indice_satelite, 2]
    af0 = Ephem[indice_satelite, 17]    # Correction horloge ordre 0
    af1 = Ephem[indice_satelite, 18]    # Correction horloge ordre 1
    af2 = Ephem[indice_satelite, 19]    # Correction horloge ordre 2
    toe = Ephem[indice_satelite, 1]
    toc = Ephem[indice_satelite, 20]    # Temps de l'horloge du satellite
    deltan = Ephem[indice_satelite, 9]
    M0 = Ephem[indice_satelite, 6]

    n0 = (mu / a ** 3) ** 0.5

    N = n0 + deltan

    tk = t - toe

    tk += 604800 * (2 * (tk < 302400) - 1)
    # if tk > 302400:       #procédure pour les problèmes de transition d'une semaine à l'autre
    #     tk = tk - 604800
    # elif tk < -302400:
    #     tk = tk + 604800

    Mk = M0 + N * tk

    Ek = Mk

    while abs(Mk - Ek + ecc * sin(Ek)) > 10 ** -12:  #boucle de calcul de Ek

        Ek = Ek - (Ek - ecc * sin(Ek) - Mk) / (1 - ecc * cos(Ek))

    DeltaR = F*ecc*a ** 0.5 * sin(Ek) # Terme de correction relativiste

    corPR = af0 + af1*(t-toc) + af2*(t-toc) ** 2 + DeltaR

    return corPR
