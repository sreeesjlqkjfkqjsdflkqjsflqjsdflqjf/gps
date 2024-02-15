# -------------------------------------------------------------------------
#
#                   Formater les données du ublox M8T
# 
# -------------------------------------------------------------------------

# les fichiers s'appellent ici "ubx data Mobile" et "ubx data SB", chacun
# doit contenir les informations de pseudodistances, de mesure de phase,
# ainsi que les éphémérides des satellites. Ils doivent avoir la même base
# de temps.

# Attention : les fichiers doivent être au format xslx sinon il n'y a pas 
# assez de colonnes ! 

# Tableau des éphémérides
# 24 paramètres d'éphéméride : 
# PRN, TOE, Eccentricité, i0, omega0, omega, M0, idot, omegadot, deltan,
# cuc, cus, crc, crs, cic, cis, racine(a),af0,af1,af2, Toc, tgd, iodc, iode

import numpy as np
from tp2.read_csv import read_csv, _float

n_ech_max = 1000  # on autorise au max 1000 échantillon
t0_GPS = 222602  # temps GPS initial

# On récupère les éphémérides du fichiers excel
T = read_csv('../../ubx data(ephemeris_data).csv', value_split=';')[1:-1]

Ephem = np.zeros((32, 24))
for t in T:
    index = int(t[0])
    Ephem[index-1, :] = tuple(map(_float, t[:24]))

T = read_csv('../../ubx data(psr_cp_data).csv', value_split=';')[1:-1]

for line in T:
    line[:] = line[:4 * n_ech_max] + [''] * max(0, 4 * n_ech_max - len(line))

satellites = [0] * 32
for line in T:
    for index in range(1, 4*n_ech_max, 4):
        if line[index]:
            satellites[int(line[index])-1] = 1
# satellites captés
satellites[:] = filter(lambda x: satellites[x-1], range(1, 33))

DonneesPR = np.zeros((n_ech_max, 2 * len(satellites) + 1))
for column in range(0, 4*n_ech_max, 4):
    if not T[0][column]:
        continue
    DonneesPR[column // 4, 0] = round(_float(T[0][column]))
    for line in T:
        if not line[column]:
            continue
        sat_index = 2 * satellites.index(int(line[column+1])) + 1
        pseudo_dist = _float(line[column+2])
        phase = _float(line[column+3])
        DonneesPR[column // 4, sat_index:sat_index+2] = pseudo_dist, phase

t_init = np.argmax(DonneesPR[:, 0] >= t0_GPS)
if DonneesPR[-1, 0] == 0.:
    t_max = np.argmin(DonneesPR[:, 0] > 0.)
else:
    t_max = n_ech_max
nb_tot = int(DonneesPR[t_max-1, 0] - t0_GPS)

DonneesPRFormat = np.zeros((nb_tot, 2 * len(satellites) + 1))
for i in range(nb_tot):
    t_test, t_rec = t0_GPS + i, t_init
    while t_rec < nb_tot and DonneesPR[t_rec, 0] != t_test:
        t_rec += 1
    if t_rec < nb_tot:
        DonneesPRFormat[i, :] = DonneesPR[t_rec, :]
    else:
        DonneesPRFormat[i, 0] = t_test

DonneesPR = DonneesPRFormat[:nb_tot, :]
PRCode = np.zeros((len(satellites), nb_tot))
for time_index in range(nb_tot):
    for sat_index in range(len(satellites)):
        if DonneesPR[time_index, 2 * sat_index] > 0.:
            PRCode[sat_index, time_index] = DonneesPR[time_index, 2 * sat_index]

nbSatDispo = np.sum(PRCode > 0., axis=0)

"""

#### On constitue un tableau qui indique lorsque les satellites
#### seront disponibles ou pas, ainsi qu'un tableau PRCode qui contient les
#### pseudodistances des satellites utile rangées ordre croissant

SatDispo = ones(t_total,nmax)

PRCode = zeros(nmax,t_total)

n=1

for i=1:t_total
    for j=1:nmax
        if DonneesPR(i,2*j) == 0                            # Si la pseudodistance n'est pas pas disponible, alors on met un 0
            SatDispo(i,j) = 0

        else
            PRCode(j,i) = DonneesPR(i,2*j)                 # Sinon on remplit PRCode

        end
    end
end

nbSatDispo = sum(SatDispo,2)                               # On connaît ainsi le nombre de satellites disponibles à chaque instant, utile pour gérer les pertes de données dans les boucles
"""
