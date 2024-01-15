"""
%--------------------------------------------------------------------------
%
%Programme TD  # 2 -4 Calcule position satellite avec
%ephemerides - à compléter
%
%--------------------------------------------------------------------------
"""
import numpy as np
from ..read_csv import get_ephemeride, get_pseudodist
from .Correction_Horloge_Satellite import Correction_Horloge_Satellite

c = 299792458  # %vitesse de la lumière
t0_GPS = 28800  # %temps GPS initial

t_total = 100 # %temps total de calcul
nSat = 4 # %Nombre de Satellites

temps = np.arange(t0_GPS, t0_GPS + t_total)

# %On connait la vraie position du point

Position = [
    [4212020.6150],
    [212020.4570],
    [4769002.0090],
]

CorPRHorlSatpoint = np.zeros((nSat, t_total), float)
PosSat = np.zeros((nSat * 3, t_total), float)

# %On suppose qu'on connait les pseudodistances qui sont dans les données

Eph = get_ephemeride()

PRCode = get_pseudodist()

for date in temps:

    # %Boucle de calcul de position des satellites

    for sat_index in range(nSat):
        tgd = Eph[21, sat_index]  # %Temps de groupe(retard du à l'electronique du satellite)

        # % On calcule les erreurs d'horloge et effets relativistes, on lui retire tgd, soit le 22ième paramètre du tableau Eph et on corrige la pseudodistance

        # % ** ** ** ** étape  # 1 à compléter
        correction = Correction_Horloge_Satellite(date, Eph) - tgd
        PRCode[sat_index, date] += correction
        # % Calcul de la position du satellite(Repère ECEF)

        # % ** ** ** ** étape  # 2 à compléter

        # % Calcul de la position du satellite(Référentiel ECEF)

        # % ** ** ** ** étape  # 3 à compléter
