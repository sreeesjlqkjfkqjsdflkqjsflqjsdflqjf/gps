import matplotlib.pyplot as plt
import numpy as np


RT = 6400e3
SAT_DISTANCE = RT + 20200e3
C_SPEED = 3.e8


def solve_receptor_position(*satellites, epsilon=1e0):
    sat_arr = np.array(satellites)
    phi, theta, rho = sat_arr[:, 0], sat_arr[:, 1], sat_arr[:, 2]

    vector, iterating = np.zeros((4, 1), float), True
    while iterating:
        # shape: (3,)
        rec_pos = vector[0:3, 0]
        # shape: (4, 3)
        sat_pos = SAT_DISTANCE * np.array([np.cos(theta) * np.cos(phi), np.cos(theta) * np.cos(phi), np.sin(theta)]).transpose()
        # shape (4,)
        rj = np.sum((sat_pos - rec_pos[None, :]) ** 2, axis=1) ** .5
        # shape: (4, 3)
        aj = sat_pos - rec_pos[None, :] / rj[:, None]

        # Jacobian shape: (4, 4)
        J = np.concatenate((aj, - C_SPEED * np.ones((4, 1), float)), axis=1)
        dp = np.linalg.inv(J) @ vector
        vector += dp
        iterating = np.sum(dp ** 2) <= epsilon ** 2

    dt = vector[3, 0]
    rec_pos = vector[0:3, 0]
    r = np.sum(rec_pos ** 2) ** .5
    alt = r - RT
    rec_pos /= r
    rec_theta = np.arcsin(rec_pos[-1])
    rec_pos *= (1 - rec_pos[-1] ** 2) ** -.5
    rec_phi = np.arccos(rec_pos[0]) * (2 * (rec_pos[1] > 1) - 1)
    return rec_phi, rec_theta, alt, dt
