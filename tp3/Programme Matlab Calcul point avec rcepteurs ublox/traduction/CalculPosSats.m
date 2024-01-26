%--------------------------------------------------------------------------
%
%           Programme pour calculer les positions des satellites (et donc
%           du point)           
%
%--------------------------------------------------------------------------

% Le calcul de position va être effectué dans la même boucle que la position
% des satellites

% On initialise l'algorithme
epsilon = 1e-4;                             % la condition d'arrêt est évaluée à 10^-4

PositionsCalculees = zeros(4,t_total);      % Cette variable contient les positions calculées par l'algorithme

HDOP = zeros(1,t_total);                    % Tableau de HDOP
VDOP = zeros(1,t_total);                    % Tableau de VDOP
TDOP = zeros(1,t_total);                    % Tableau de TDOP

PosSat = zeros(3*nmax,t_total);             % Pour conserver les positions calculées des satellites
Residus = zeros(3*nmax,t_total);            % Pour conserver les résidus calculés

% Combine pour retirer des satellites

SatDispoCons = SatDispo;     % On conserve les satDispo tel qu'ils sont
nbSatDispoCons = nbSatDispo;

% On cherche où est le satellite dans la liste
indSatSupr1 = 1;
indSatSupr2 = 1;
indSatSupr3 = 1;
indSatSupr4 = 1;

for n=1:nmax

    if numeroSat(n) == 7  % J'enlève les satellites 7 et 8 par exemple

        indSatSupr1 = n;

    end

    if numeroSat(n) == 8  

        indSatSupr2 = n;

    end

    if numeroSat(n) == 30 % J'enlève les satellites 7 et 8 par exemple

        indSatSupr3 = n;

    end

    if numeroSat(n) == 20  

        indSatSupr4 = n;

    end
end

SatDispo(:,indSatSupr1) = zeros(1,t_total);   % On met des 0 là où on veut que le satellite soit supprimé
SatDispo(:,indSatSupr2) = zeros(1,t_total);   % On met des 0 là où on veut que le satellite soit supprimé
%SatDispo(:,indSatSupr3) = zeros(1,t_total);   % On met des 0 là où on veut que le satellite soit supprimé
% SatDispo(:,indSatSupr4) = zeros(1,t_total);   % On met des 0 là où on veut que le satellite soit supprimé

nbSatDispo = sum(SatDispo,2);                % On met à jour le nombre de satellites disponibles


for t=1:t_total
   
    if nbSatDispo(t) > 3                    % On calcule le point s'il y a assez de satellites

        % Boucle pour corriger les erreurs sur les pseudodistances liées aux horloges satellites avant le lancement du calcul
        % du point
        
        % pour l'instant t, on crée des tableaux qu'on va utiliser

        nSat = nbSatDispo(t);               % le nombre de satellites utilisables pour l'instant considéré
    
        PRCodeCalSat = zeros(nSat,1);       % les pseudodistances code utilisées pour le calcul
        Eph = zeros(nSat,24);               % Tableau d'éphémérides des satellites utilisables
        PosSat_t = zeros(nSat*3,1);         % Positions des satellites utilisables
    
        n=1;
        for i=1:nmax
    
            if SatDispo(t,i) == 1           % Si le satellite est disponible alors on inclut sa pseudodistance et ses éphémérides dans les variables utiles pour le calcul 
    
                PRCodeCalSat(n) = PRCode(i,t);
                Eph(n,:) = Ephem(numeroSat(i),:);
    
                n=n+1;
    
            end
    
    
        end
    
        % Correction des pseudodistances
    
        for n=1:nSat
    
            tgd = Eph(n,22);              % Temps de groupe (retard du à l'electronique du satellite)
    
            % On calcule les erreurs d'horloge et effets relativistes, on lui retire tgd, soit le 22ième paramètre du tableau Eph
    
            corPR = Correction_Horloge_Satellite(temps(t),  Eph(n,:))-tgd;
            
            % On corrige la pseudodistance
            pseudodist = PRCodeCalSat(n)+c*corPR;                               % On récupère la pseudodistance corrigée     
            PRCodeCalSat(n) = pseudodist;                                       % On stocke la pseudodistance corrigée de ces effets
    
        end
    
        % Boucle de calcul de la position
    
    
        PtHyp = zeros(4,1);                 % le point hypothèse est initialisé à 0,0,0,0 (en incluant le biais d'horloge)
    
        diff = [1;1;1;1];                   % la variable qui va contenir la variation entre le nouveau point hypothèse et le point hypothèse précédent.
    
        H = [zeros(nSat,3),ones(nSat,1)];   % la matrice d'observation H
    
        PRhyp = zeros(nSat,1);              % les pseudodistances hypothèses résultantes
    
        tr=1;                               % Une variable pour compter les tours de boucle
    
        BiaisH = 0;                         % On ne connait pas le biais à priori, donc on met 0
        
        while norm(diff) > epsilon && tr < 10  % On reboucle tant que la norme de diff est plus grande que epsilon ou que le nombre de boucle est plus petit que 10
        
            % Détermination des coordonnées des satellites 
    
            for n = 1:nSat     
    
    
                pseudodist = PRCodeCalSat(n);         % La pseudodistance utilisée est récupérée depuis le tableau de PR établi précédemment  
                dpropag = pseudodist -BiaisH;         % La distance de propagation est calculée en retirant la valeur actualisée du biais à la pseudodistance
          
                % Calcul de la position du satellite (Repère ECEF)
        
                [Xs, Ys, Zs] = CalculEphemeride(temps(t)-dpropag/c,Eph(n,:));
        
                % Calcul de la position du satellite (Référentiel ECEF)
        
                Rot_X = e_r_corr(dpropag/c, [Xs;Ys;Zs]);
        
                Xs = Rot_X(1);
                Ys = Rot_X(2);
                Zs = Rot_X(3);
        
                PosSat_t(3*(n-1)+1,1)= Xs;
                PosSat_t(3*(n-1)+2,1)= Ys;
                PosSat_t(3*(n-1)+3,1)= Zs;       
    
            end
    
            % On construit la matrice H, on commence par calculer les distances résultantes
    
            dist = zeros(nSat,1);
    
            for n = 1:nSat
        
                dist(n) = ( sum((PosSat_t(3*(n-1)+1:3*(n-1)+3,1)-PtHyp(1:3,1)).^2) )^0.5; 
         
            end
    
            % On établit la matrice H ligne par ligne
    
            for n=1:nSat
    
                for j=1:3
                    H(n,j) = ( PosSat_t(3*(n-1)+j,1)-PtHyp(j,1) )/dist(n);
                end
    
            end
            % On établit le vecteur de mesures qu'on obtiendrait si la position était au point hypothèse
        
            PRhyp = dist + PtHyp(4,1)*ones(nSat,1);
        
            % On obtient le vecteur DeltaPR (deltaRo)
        
            DeltaPR = PRhyp - PRCodeCalSat;
        
            % On inverse la matrice H et on calcule le vecteur diff
    
            if abs(det(H'*H))> eps 
        
                diff = inv(H'*H)*H'*DeltaPR;
        
                % On met à jour le point hypothèse
            
                PtHyp = PtHyp+[diff(1:3);-1*diff(4)];   % Ici on fait bien attention à ajouter -1*diff(4) car structurellement c'est l'opposé de la différence du biais d'horloge qu'on calcule
                BiaisH  = PtHyp(4);
            else             % Si le déterminant est vraiment trop petit, cela veut dire que la matrice est singulière : on ne calcule pas le point
                PtHyp = [NaN;NaN;NaN;NaN];
                tr=10;
            end
        
            tr=tr+1;
    
        end
    
       PositionsCalculees(:,t) = PtHyp;
       
    
       % On calcule la DOP à la fin du calcul. On est obligé de faire un
       % changement de repère pour que les notions d'horizontale et verticale
       % ait un sens

       CoordSatNr = zeros(3*nSat,1);
        
       for i =1:nSat
    
            % changement de repère pour les satellites
    
            X = PosSat_t((i-1)*3+1,1);
            Y = PosSat_t((i-1)*3+2,1);
            Z = PosSat_t((i-1)*3+3,1);
    
            [X,Y,Z] = ChangeRep(X,Y,Z,PositionsCalculees(1,t),PositionsCalculees(2,t),PositionsCalculees(3,t),long,lat);
    
            CoordSatNr((i-1)*3+1,1) = X;
            CoordSatNr((i-1)*3+2,1) = Y;
            CoordSatNr((i-1)*3+3,1) = Z;
       end
            
       % On calcul la matrice H correspondante 
    
       H = [zeros(nSat,3),ones(nSat,1)];   % la matrice d'observation H
    
       dist = zeros(nSat,1);
    
        for n = 1:nSat
    
            dist(n) = ( sum((CoordSatNr(3*(n-1)+1:3*(n-1)+3,1)).^2) )^0.5; 
       
        end
    
        % On établit la matrice H ligne par ligne
    
        for n=1:nSat
    
            for j=1:3
                H(n,j) = ( CoordSatNr(3*(n-1)+j,1) )/dist(n);
            end
    
        end
    
        % On calcule la matrice pour la DOP
        
        MatDop = inv(H'*H); 
    
        HDOP(t) = (MatDop(2,2)+MatDop(3,3))^0.5;
        VDOP(t) = MatDop(1,1)^0.5;
        TDOP(t) = MatDop(4,4)^0.5;
   
        % On stocke les coordonnées des satellites calculées
        u=1;
        for n=1:nmax
    
            if SatDispo(t,n) == 1
    
                PosSat(3*(n-1)+1,t) = PosSat_t(3*(u-1)+1,1);
                PosSat(3*(n-1)+2,t) = PosSat_t(3*(u-1)+2,1);
                PosSat(3*(n-1)+3,t) = PosSat_t(3*(u-1)+3,1);
                u=u+1;
    
            end
    
        end

        % On calcule les résidus

        X = PositionsCalculees(1,t);
        Y = PositionsCalculees(2,t);
        Z = PositionsCalculees(3,t);
        DT = PositionsCalculees(4,t);

        u=1;
        for n=1:nmax
            
            if SatDispo(t,n) == 1
    
                Xs = PosSat(3*(n-1)+1,t);
                Ys = PosSat(3*(n-1)+2,t);
                Zs = PosSat(3*(n-1)+3,t);

                PRobt = ((Xs-X)^2+(Ys-Y)^2+(Zs-Z)^2)^0.5+DT;

                Residus(n,t) = PRobt-PRCodeCalSat(u);    % Le résidu est la différence entre la pseudodistance mesurée et celle qu'on devrait obtenir si on se situe bien au point calculé
                u=u+1;
  
            end
    
        end      

    end
end

% Une fois qu'on a fini on remet les indicateurs à la normale

SatDispo = SatDispoCons;    
nbSatDispo = nbSatDispoCons;




    
    