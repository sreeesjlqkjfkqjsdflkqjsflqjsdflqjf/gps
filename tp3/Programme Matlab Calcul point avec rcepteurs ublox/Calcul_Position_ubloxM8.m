%--------------------------------------------------------------------------
%
%           Programme Calcul position avec les Pseudodistances code
%
%--------------------------------------------------------------------------

clear

c =299792458;       % vitesse de la lumière

f= 1575420000;      % fréquence L1

t0_GPS = 222602;     % temps GPS initial

t_total = 0;      % temps total de calcul

nSat = 0;           % Nombre de Satellites

% On formate les données issues des deux fichiers xlsx "ubx data Mobile" et "ubx data SB"

FormaterDonneesM8


temps = t0_GPS:t0_GPS+t_total-1;

% On peut ici mettre la vraie position d'un point qu'on teste (par exemple)

lat = 48.71368917;
long = 2.20036217;
alt = 197.2;

[X, Y, Z] = CoordGeograph_Cart(lat,long,alt);

PositionCent = [X;   Y;  Z];

CorPRHorlSatpoint = zeros(nSat,t_total);
PosSat = zeros(nSat*3,t_total);

% Calcul de la position du point avec le code et les positions des satellites

CalculPosSats

% ----- On centre le repère sur la vrai position

Xcent = PositionCent(1);
Ycent = PositionCent(2);
Zcent = PositionCent(3);

[lat, long, alt] = CoordCart_Geograph(Xcent,Ycent,Zcent);   % On a besoin de récupérer la latitude et la longitude pour faire les rotations

ErreurPositionH = zeros(2,t_total);             % Cette variable nous donne la valeur en mètres de l'erreur horizontale
ErreurPositionV = zeros(1,t_total);             % Cette variable nous donne la valeur en mètres de l'erreur verticale

for t=1:t_total

    if nbSatDispo(t,1) > 3          % On ne calcule l'erreur que si la position a été calculée, cela vaut 0 sinon

        [X,Y,Z] = ChangeRep(PositionsCalculees(1,t),PositionsCalculees(2,t),PositionsCalculees(3,t),Xcent,Ycent,Zcent,long,lat);
    
        ErreurPositionH(:,t) = [Y;Z];  % le changement de repère est fait de telle sorte que l'horizontale se trouve en Y,Z et la verticale en X
        ErreurPositionV(t) = X;

    end

end

% On affiche les satellites sur la figure de projection

AfficheSats

% On affiche l'erreur horizontale

% Calcul des erreurs 

ErreurHoriz = (ErreurPositionH(1,:).^2+ ErreurPositionH(2,:).^2).^0.5;

axeymax = (max(ErreurHoriz)-mod(max(ErreurHoriz),10))+10;
axeymin = (min(ErreurHoriz)-mod(min(ErreurHoriz),10));

figure('Name','Erreur avec PR Code Horiz ')
plot(temps,ErreurHoriz,'-*','MarkerSize',1)
axis([temps(1) temps(t_total) axeymin axeymax ])
grid

legend('Erreur Horizontale')

% Conversion en latitude longitude pour affichage sur fond de carte

PositionsGeograph = zeros(2,t_total);

for t=1:t_total

    if abs(PositionsCalculees(1,t)) > 0                 % On ne fait la conversion que sur des points effectivement calculés (non égal à 0), sinon l'algorithme ne converge pas

      [lat,long,alt] = CoordCart_Geograph(PositionsCalculees(1,t),PositionsCalculees(2,t),PositionsCalculees(3,t));
      PositionsGeograph(:,t) = [lat;long];

    else
        PositionsGeograph(:,t) = PositionsGeograph(:,t-1);      % Si on n'a pas de point, on répète le précédent pour que le fichier n'ait pas de trou
    end

end

% Formatage pour le fichier xsl

PositionLat_Lon = PositionsGeograph(:,1:t_total)';


