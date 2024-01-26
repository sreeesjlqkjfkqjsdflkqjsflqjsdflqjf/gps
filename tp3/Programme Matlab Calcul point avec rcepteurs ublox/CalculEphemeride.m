%--------------------------------------------------------------------------
% Fonction pour calculer les coordonn�es des satellites � partir des
% �ph�m�rides en fonction du temps GPS qui correspond � l'instant de d�part
% du signal
%
%--------------------------------------------------------------------------

function [Xs, Ys, Zs] = CalculEphemeride(t_GPS,Ephem)

%Pi = 3.1415926535898;  % on d�finit Pi avec le bon nombre de d�cimales

mu = 398600500000000;              % Constante li�e � la gravitation de la Terre
omegadote = 7.2921151467 * 10^-5;  % Constante vitesse de rotation de la terre

toe = Ephem(2);               % Temps GPS � partir duquel les �ph�m�rides sont valables
ecc = Ephem(3);               % Excentricit� de la trajectoire
i0 = Ephem(4);                % Inclinaison � l'instant toe
omega0 = Ephem(5);            % Longitude du noeud ascendant
omega = Ephem(6);             % Argument du p�rig�e � l'instant toe
M0 = Ephem(7);                % Anomalie moyenne
idot = Ephem(8);              % Taux de variation de l'inclinaison 
omegadot = Ephem(9);          % Taux de variation de la longitude du noeud ascendant  
deltan = Ephem(10);           % Correction du mouvement moyen
cuc = Ephem(11);              % Amplitude du cosinus de correction � l'argument de la latitude
cus = Ephem(12);              % Amplitude du sinus de correction � l'argument de la latitude
crc = Ephem(13);              % Amplitude du cosinus de correction du rayon orbital
crs = Ephem(14);              % Amplitude du sinus de correction du rayon orbital
cic = Ephem(15);              % Amplitude du cosinus de correction de l'inclinaison
cis = Ephem(16);              % Amplitude du sinus de correction de l'inclinaison
a = Ephem(17)^2;              % Demi grand axe


% Calcul de la position des satellites

n0 = (mu / a^3)^0.5;

N = n0 + deltan;

% Mise � jour du temps

tk = t_GPS - toe;       

if tk > 302400        %proc�dure pour les probl�mes de transition d'une semaine � l'autre
    tk = tk - 604800;
elseif tk < -302400
    tk = tk + 604800;
end

% Calcul de l'anomalie excentrique 

Mk = M0 + N * tk;
Ek = Mk;
%op = abs(Mk - Ek + ecc * sin(Ek));

while abs(Mk - Ek + ecc * sin(Ek)) > 10^-12   %boucle de calcul de Ek

    Ek = Ek - (Ek - ecc * sin(Ek) - Mk) / (1 - ecc * cos(Ek));
    %op = abs(Mk - Ek + ecc * sin(Ek));
end


% Applicationdes corrections orbitales

sinusVk = (sin(Ek) * (1 - ecc^2)^0.5) / (1 - ecc * cos(Ek));

cosinusVk = (cos(Ek) - ecc) / (1 - ecc * cos(Ek));
                                                                                                                                             
Phik = atan2(sinusVk, cosinusVk) + omega;

deltaPhik = cus * sin(2 * Phik) + cuc * cos(2 * Phik);
deltark = crs * sin(2 * Phik) + crc * cos(2 * Phik);
deltaik = cis * sin(2 * Phik) + cic * cos(2 * Phik);

uk = Phik + deltaPhik;
rk = a * (1 - ecc * cos(Ek)) + deltark;
ik = i0 + idot * tk + deltaik;
Omegak = omega0 + (omegadot - omegadote) * tk - omegadote * toe;
xp = rk * cos(uk);
yp = rk * sin(uk);

Xs = xp * cos(Omegak) - yp * cos(ik) * sin(Omegak);
Ys = xp * sin(Omegak) + yp * cos(ik) * cos(Omegak);
Zs = yp * sin(ik);


