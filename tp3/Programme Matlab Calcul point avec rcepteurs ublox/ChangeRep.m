% -------------------------------------------------------------------------
% 
%   Fonction pour changer de rep�re en centrant sur un point
%   (x,y,z) devient (y,z,x)
% 
% -------------------------------------------------------------------------

function [Xnrep, Ynrep, Znrep] = ChangeRep(X,Y,Z,Xcent,Ycent,Zcent,long,lat)

% on cr�e les deux matrices inverses de rotation

pinv1 = [cos(long*pi/180),sin(long*pi/180),0;-1*sin(long*pi/180),cos(long*pi/180),0;0,0,1];
pinv2 = [cos(lat*pi/180),0,sin(lat*pi/180); 0,1,0; -1*sin(lat*pi/180),0,cos(lat*pi/180)];

% on applique les rotations au point central d�sir�

PtCentral = pinv1*pinv2*[Xcent;Ycent;Zcent];

% on applique les rotations au point lui-m�me et la translation

Ptnr = pinv1*pinv2*[X;Y;Z] - PtCentral;

% on met les points

Xnrep = Ptnr(1);
Ynrep = Ptnr(2);
Znrep = Ptnr(3);


