%--------------------------------------------------------------------------
%
%           Programme pour afficher les satellites sur la figure
%          
%
%--------------------------------------------------------------------------


% On place les coordonnées dans un repère centré sur le point et tangent à
% la Terre

CoordSatNr = zeros(3*nmax,t_total);
ElAzim = zeros(2*nmax,t_total);

% Changement de repère pour tous les satellites et estimation de
% l'élévation et azimut

for t=1:t_total
    for i =1:nmax
    
        if SatDispo(t,i) == 1

            X = PosSat((i-1)*3+1,t);
            Y = PosSat((i-1)*3+2,t);
            Z = PosSat((i-1)*3+3,t);
    
            [X,Y,Z] = ChangeRep(X,Y,Z,Xcent,Ycent,Zcent,long,lat);
            CoordSatNr((i-1)*3+1,t) = X;
            CoordSatNr((i-1)*3+2,t) = Y;
            CoordSatNr((i-1)*3+3,t) = Z;
    
            % projection dans le plan YZ
    
            % Calcul de l'élévation
    
            d = norm([Y,Z]);
            Elevation = atan(X/d);
            Azimut = atan2(Z,Y);
    
            ElAzim((i-1)*2+1,t) = Elevation;
            ElAzim((i-1)*2+2,t) = Azimut;

        end

    end
end

% tracé de la trajectoire des satellites

Azim = zeros(nmax,t_total);
Elev = zeros(nmax,t_total);
Xtrace = zeros(nmax,t_total);
Ytrace = zeros(nmax,t_total);

for t=1:t_total

    for i=1:nmax

       if SatDispo(t,i) == 1                % Si le saltellite est disponible on le trace
            
            X = CoordSatNr((i-1)*3+1,t);
            Y = CoordSatNr((i-1)*3+2,t);
            Z = CoordSatNr((i-1)*3+3,t);    
            d = norm([Y,Z]);
            Elevation = atan(X/d);
            Azimut = atan2(Z,Y);
    
            % mise en forme pour tracé 
            Azim(i,t)= Azimut;
            Elev(i,t)=Elevation*180/pi;
    
            Xtrace(i,t) = (90-Elev(i,t))*cos(Azim(i,t));
            Ytrace(i,t) = (90-Elev(i,t))*sin(Azim(i,t));

       else                                  % Si le satellite n'est pas disponible, on met un NaN pour que cela ne trace rien
            
            Xtrace(i,t) = NaN;
            Ytrace(i,t) = NaN;

       end

    end
end

% Préparation du tracé

val = (1:101)/(100);
figure

% On trace les trajectoires

plot(Xtrace,Ytrace,'o','MarkerSize',1)

% On met des cercles pour que ce soit joli et lisible

axis([-90 90 -90 90])
hold on
plot(90*cos(2*pi*val),90*sin(2*pi*val))
plot(45*cos(2*pi*val),45*sin(2*pi*val))
plot(20*cos(2*pi*val),20*sin(2*pi*val))

for i = 1:nmax

    textesat = ['S' num2str(numeroSat(i),'%02d')];

    u= t_total; % Pour écrire le numéro du satellite, on cherche le dernier instant u où le satellite était présent
    while SatDispo(u,i) == 0

        u=u-1;

    end
    
    text(Xtrace(i,u),Ytrace(i,u),textesat)
end

hold off