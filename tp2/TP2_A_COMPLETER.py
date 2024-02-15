"""
%--------------------------------------------------------------------------
%
%Programme TD  # 2 -4 Calcule position satellite avec
%ephemerides - à compléter
%
%--------------------------------------------------------------------------
"""
import numpy as np
from read_csv import get_ephemeride, get_pseudodist
from traduction.Correction_Horloge_Satellite import Correction_Horloge_Satellite
from traduction.CalculEphemeride import CalculEphemeride
from traduction.e_r_corr import e_r_corr

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
    indice_temps = date - t0_GPS
    # %Boucle de calcul de position des satellites

    for sat_index in range(nSat):
        tgd = Eph[sat_index, 21]  # %Temps de groupe(retard du à l'electronique du satellite)

        # % On calcule les erreurs d'horloge et effets relativistes, on lui retire tgd, soit le 22ième paramètre du tableau Eph et on corrige la pseudodistance

        # % ** ** ** ** étape  # 1 à compléter
        correction = Correction_Horloge_Satellite(date, Eph, sat_index) - tgd
        PRCode[sat_index, indice_temps] += c * correction
        # % Calcul de la position du satellite(Repère ECEF)

        # % ** ** ** ** étape  # 2 à compléter
        date_emission_satellite = date - PRCode[sat_index, indice_temps] / c
        position_err_rotation = CalculEphemeride(date_emission_satellite, Eph, sat_index)
        position_satellite = e_r_corr(PRCode[sat_index, indice_temps], position_err_rotation)

        # % Calcul de la position du satellite(Référentiel ECEF)

        # % ** ** ** ** étape  # 3 à compléter
