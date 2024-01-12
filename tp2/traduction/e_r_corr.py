"""
%--------------------------------------------------------------------------
% Fonction qui permet de calculer les coordonnées obtenue en faisant la rotation
% inverse de la Terre pendant la durée en entrée
%
%--------------------------------------------------------------------------
"""
import numpy as np
from numpy import cos, sin


def e_r_corr(traveltime, X_sat):
    # function X_sat_rot = e_r_corr(traveltime, X_sat)
    """
    %E_R_CORR  Returns rotated satellite ECEF coordinates due to Earth
    %rotation during signal travel time
    %
    %X_sat_rot = e_r_corr(traveltime, X_sat);
    %
    %   Inputs:
    %       travelTime  - signal travel time
    %       X_sat       - satellite's ECEF coordinates
    %
    %   Outputs:
    %       X_sat_rot   - rotated satellite's coordinates (ECEF)
    """
    """
    %Written by Kai Borre
    %Copyright (c) by Kai Borre
    %
    % CVS record:
    % $Id: e_r_corr.m,v 1.1.1.1.2.6 2006/08/22 13:45:59 dpl Exp $
    %==========================================================================
    """
    Omegae_dot = 7.292115147e-5           #  rad/sec

    # %--- Find rotation angle --------------------------------------------------
    omegatau = Omegae_dot * traveltime

    # %--- Make a rotation matrix -----------------------------------------------
    R3 = np.array([
        [cos(omegatau), sin(omegatau),   0],
        [-sin(omegatau), cos(omegatau), 0],
        [0, 0, 1]
    ])

    # %--- Do the rotation ------------------------------------------------------
    X_sat_rot = R3 @ X_sat
    return X_sat_rot