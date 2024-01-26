% -------------------------------------------------------------------------
%
%                   Formater les données du ublox M8T
% 
% -------------------------------------------------------------------------

% les fichiers s'appellent ici "ubx data Mobile" et "ubx data SB", chacun
% doit contenir les informations de pseudodistances, de mesure de phase,
% ainsi que les éphémérides des satellites. Ils doivent avoir la même base
% de temps.

% Attention : les fichiers doivent être au format xslx sinon il n'y a pas 
% assez de colonnes ! 

% Tableau des éphémérides
% 24 paramètres d'éphéméride : 
% PRN, TOE, Eccentricité, i0, omega0, omega, M0, idot, omegadot, deltan,
% cuc, cus, crc, crs, cic, cis, racine(a),af0,af1,af2, Toc, tgd, iodc, iode

nechmax = 1000;                                                 % on autorise au max 1000 échantillon

T = readtable('ubx data.xlsx', 'Sheet',3, 'Range','A1:X33');    % On récupère les éphémérides du fichiers excel

Ephemprov = T{1:32,1:24};                                       % On copie de la structure vers un tableau exploitable

% Mise en forme du tableau d'éphémérides : on cherche les satellites dont
% on dispose des éphémérides

for i=1:32    
    if isnan(Ephemprov(i,1))
       Ephemprov(i,1) =0; 
    end    
end


% On crée un tableau Ephemprov de 32 lignes dont chacune correspond à un des 32 satellites GPS 

Ephem = zeros(32,24);

for i=1:32

    if Ephemprov(i,1) ~= 0

        Ephem(Ephemprov(i,1),:) = Ephemprov(i,:);
        
    end

end

Ephemprov = Ephem; 

% Mise en forme du tableau pour l'algorithme

Ephem = Ephemprov(:,1);                 % Numéro du satellite
Ephem = [ Ephem Ephemprov(:,17)];       % Time of Ephemeride (date de validité)
Ephem = [ Ephem Ephemprov(:,4)];        % excentricité
Ephem = [ Ephem Ephemprov(:,7)];        % i0
Ephem = [ Ephem Ephemprov(:,6)];        % omega0
Ephem = [ Ephem Ephemprov(:,8)];        % omega
Ephem = [ Ephem Ephemprov(:,2)];        % M0
Ephem = [ Ephem Ephemprov(:,10)];       % idot
Ephem = [ Ephem Ephemprov(:,9)];        % omegadot
Ephem = [ Ephem Ephemprov(:,3)];        % deltan
Ephem = [ Ephem Ephemprov(:,11:16)];    % cuc,cus,crc,crs,cic,cis
Ephem = [ Ephem Ephemprov(:,5)];        % racine(a)
Ephem = [ Ephem Ephemprov(:,21:23)];    % afo,af1,af2
Ephem = [ Ephem Ephemprov(:,20)];       % toc
Ephem = [ Ephem Ephemprov(:,24)];       % tgd
Ephem = [ Ephem Ephemprov(:,19)];       % iodc
Ephem = [ Ephem Ephemprov(:,18)];       % iode

% Ephem est prête à servir pour le calcul des positions des satellites

% Tableau des Pseudodistances et des mesures de Phase de porteuse de la
% station de base
% Paramètre : Tgps,PRsat1,CPsat1,PRsat2,CPsat2,...PRsatN,CPsatN) 

T = readtable('ubx data.xlsx','Sheet',1, 'Range','A1:EWV13'); % Calibré pour 1000 secondes et 12 satellites

DonneesPRprov = T{1:12,1:nechmax*4};

for i=1:12
    for j = 1:nechmax*4
        if isnan(DonneesPRprov(i,j))
            DonneesPRprov(i,j) = 0; 
        end
    end
end

% formatage des données sous la forme d'un tableau comme indiqué
% Le numéro du satellite correspondant sera indiqué dans le tableau 
% "numeroSat". 
% Premier balayage pour lister les satellites


numeroSat = zeros(1,32);  % on n'en aura que 12, mais les trente deux pourraient apparaître (un enregistrement très très long)

i = 1;
while   i <= 12 && DonneesPRprov(i,2) > 0            % on crée la première liste à partir de la première colonne
    numeroSat(i)=DonneesPRprov(i,2);
    i=i+1;
end
nmax = i-1;

% Maintenant il faut balayer tout l'enregistrement pour vérifier si
% d'autres satellites ne sont pas apparus

for j = 6:4:4*nechmax-2
    for i = 1:12
        if DonneesPRprov(i,j) > 0        % condition pour que le test soit fait
            estla = 0;                       % drapeau indiquant si le satellite a déjà été rencontré ou pas
            for k = 1:nmax
                if DonneesPRprov(i,j) == numeroSat(k)      
                    estla = 1;              % le satellite a déjà été recensé
                end
            end

            if estla == 0                   % si le drapeau n'a pas bougé, c'est que le satellite est nouveau pour nous
                nmax = nmax+1;
                numeroSat(nmax) = DonneesPRprov(i,j);
            end
        end        
    end
end


% On s'assure qu'on dispose bien des éphémérides de chaque satellite
% recensé sinon on l'exclut

numeroSat2 = zeros(1,32);
u=1;
for i=1:nmax
    
    if Ephem(numeroSat(i),1) > 0  

        numeroSat2(u) = numeroSat(i);
        u=u+1;
    end
    
end

numeroSat = numeroSat2;
nmax=u-1;

% On les trie du plus petit numéro au plus grand

for pluspetit= 1:nmax-1
    for j = pluspetit+1:nmax
        if numeroSat(j) < numeroSat(pluspetit)
            a = numeroSat(pluspetit);
            numeroSat(pluspetit) = numeroSat(j);
            numeroSat(j) = a;
        end
    end 
end

% On a recensé tous nos satellites, maintenant on met en forme le tableau
DonneesPR = zeros(nechmax,1+nmax*2);
jj = 1;
for j = 1:4:4*nechmax-3
    DonneesPR(jj,1) = round(DonneesPRprov(1,j));  % le temps GPS correspondant (arrondi à l'entier le plus proche)
    for i = 1:nmax                            % pour chaque satellite recensé
        ii = 1;
        while ii <= 12                        % on regarde s'il se trouve dans la colonne
            if numeroSat(i) == DonneesPRprov(ii,j+1)            % si un satellite correspond
                DonneesPR(jj,2*(i-1)+2) = DonneesPRprov(ii,j+2);  % on met la pseudodistance
                DonneesPR(jj,2*(i-1)+3) = DonneesPRprov(ii,j+3);  % on met la mesure de phase
            end  
            ii = ii+1;
        end
        
    end
    jj=jj+1;
end

%%%% On doit maintenant gérer les éventuelles pertes de données lors de la
%%%% récupération.

% détermination de l'indice de l'instant initial pour le récepteur

tinit = 1;

while (DonneesPR(tinit,1) ~= t0_GPS)  % on avance à partir de 1 jusqu'à ce que ce soit égal
    tinit = tinit +1;
end


% On doit maintenant vérifier que les données sont bien calées sur le même
% temps, des erreurs pouvant survenir (on rate un échantillon ou on a un doublon)

tmax = 1;
while DonneesPR(tmax,1) ~= 0 && tmax < nechmax+1   % l'indice max du temps
    tmax = tmax+1;
end
tmax = tmax-1;

tmin = DonneesPR(tmax,1);                                 % On se cale sur le plus petit des deux
nbtot = tmin - t0_GPS;                                    % le nombre total d'échantillons attendus 

DonneesPRformat = zeros(tmax,2*nmax+1);

for i = 0:nbtot
    ttest = t0_GPS + i;                                    % le temps qu'il faut tester

    % on teste
    trec = tinit;                                          % A chaque fois on repart du temps initial, pas optimal mais sûr
    while DonneesPR(trec,1) ~= ttest && trec < tmax+1      % boucle dont on sort soit lorsqu'on a trouvé le temps correspondant, soit si on est au bout de la recherche
        trec = trec+1;
    end
    if trec < tmax +1                                       % si on est sorti parce qu'on a trouvé le temps
       DonneesPRformat(i+1,:) = DonneesPR(trec,:);          % On le récupère
    else                                                    % Si on ne l'a pas trouvé
       DonneesPRformat(i+1,1) = ttest;                      % On ajoute le temps sur la ligne
       DonneesPRformat(i+1,2:2*nmax+1) = zeros(1,2*nmax);   % On associe des zéros à ce temps test
    end

end

DonneesPR = DonneesPRformat(1:1+nbtot,:);                   % mise à jour des PR

t_total = nbtot+1;                                          % Mise à jour de t_total (nombre d'échantillons total finalement considéré)


%%%% On constitue un tableau qui indique lorsque les satellites
%%%% seront disponibles ou pas, ainsi qu'un tableau PRCode qui contient les
%%%% pseudodistances des satellites utile rangées ordre croissant

SatDispo = ones(t_total,nmax);

PRCode = zeros(nmax,t_total);

n=1;

for i=1:t_total
    for j=1:nmax
        if DonneesPR(i,2*j) == 0                            % Si la pseudodistance n'est pas pas disponible, alors on met un 0
            SatDispo(i,j) = 0;

        else
            PRCode(j,i) = DonneesPR(i,2*j);                 % Sinon on remplit PRCode

        end
    end
end

nbSatDispo = sum(SatDispo,2);                               % On connaît ainsi le nombre de satellites disponibles à chaque instant, utile pour gérer les pertes de données dans les boucles

