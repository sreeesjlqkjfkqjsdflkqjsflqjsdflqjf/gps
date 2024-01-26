# --------------------------------------------------------------------------
#
#    Programme Calcul position avec les Pseudodistances code
#
# --------------------------------------------------------------------------

def main():

    # Définition des constantes
    c = 299792458  # vitesse de la lumière
    f = 1575420000  # fréquence L1
    t0_GPS = 222602  # temps GPS initial
    t_total = 0  # temps total de calcul
    nSat = 0  # Nombre de Satellites

    # Formatage des données
    FormaterDonneesM8()

    # Définition du temps
    temps = np.arange(t0_GPS, t0_GPS+t_total)

    # Définition de la position vraie
    lat = 48.71368917
    long = 2.20036217
    alt = 197.2

    # Calcul des coordonnées cartésiennes de la position vraie
    [X, Y, Z] = CoordGeograph_Cart(lat, long, alt)

    # Position du point de référence
    PositionCent = [X, Y, Z]

    # Pseudodistances entre le point de référence et les satellites
    CorPRHorlSatpoint = np.zeros((nSat, t_total))
    PosSat = np.zeros((nSat * 3, t_total))

    # Calcul de la position du point avec le code et les positions des satellites
    CalculPosSats()

    # Centrement du repère sur la position vraie
    Xcent = PositionCent[0]
    Ycent = PositionCent[1]
    Zcent = PositionCent[2]

    # Calcul de l'erreur horizontale
    ErreurPositionH = np.zeros((2, t_total))
    ErreurPositionV = np.zeros((1, t_total))

    for t in range(t_total):

        if nbSatDispo(t, 1) > 3:

            [X, Y, Z] = ChangeRep(PositionsCalculees(1, t), PositionsCalculees(
                2, t), PositionsCalculees(3, t), Xcent, Ycent, Zcent, long, lat)

            ErreurPositionH[:, t] = [Y, Z]
            ErreurPositionV[t] = X

    # Affichage de l'erreur horizontale

    # Calcul des erreurs
    ErreurHoriz = np.sqrt(ErreurPositionH[:, :].T @ ErreurPositionH[:, :])

    axeymax = (max(ErreurHoriz) - mod(max(ErreurHoriz), 10)) + 10
    axeymin = (min(ErreurHoriz) - mod(min(ErreurHoriz), 10))

    plt.figure('Name', 'Erreur avec PR Code Horiz')
    plt.plot(temps, ErreurHoriz, '-*', markersize=1)
    plt.axis([temps[0], temps[t_total], axeymin, axeymax])
    plt.grid()
    plt.legend('Erreur Horizontale')

    # Conversion en latitude longitude pour affichage sur fond de carte
    PositionsGeograph = np.zeros((2, t_total))

    for t in range(t_total):

        if abs(PositionsCalculees(1, t)) > 0:

            [lat, long, alt] = CoordCart_Geograph(PositionsCalculees(
                1, t), PositionsCalculees(2, t), PositionsCalculees(3, t))
            PositionsGeograph[:, t] = [lat, long]

        else:
            PositionsGeograph[:, t] = PositionsGeograph[:, t - 1]

    # Formatage pour le fichier xsl
    PositionLat_Lon = PositionsGeo


if __name__ == "__main__":
    main()
