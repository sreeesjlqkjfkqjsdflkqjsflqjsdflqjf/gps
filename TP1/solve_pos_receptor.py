import matplotlib.pyplot as plt
import numpy as np
from TP1.affichage import *

RT = 6400e3
SAT_DISTANCE = RT + 20200e3
LIGHT_SPEED = 3.e8
COS_TH_MAX = RT / SAT_DISTANCE


def solve_receptor_position(rng, s1, s2, s3, s4, rho1, rho2, rho3, rho4, epsilon=1e-6, real_position=(0, 0, RT, 0), max_iteration=1000, rho=1., use_err=False):
    phi_sat, theta_sat = np.array((s1, s2, s3, s4)).transpose()
    x_sat = SAT_DISTANCE * np.cos(phi_sat) * np.sin(theta_sat)
    y_sat = SAT_DISTANCE * np.sin(phi_sat) * np.sin(theta_sat)
    z_sat = SAT_DISTANCE * np.cos(theta_sat)
    if use_err:
        x_err, y_err, z_err = random_spherical_point(rng, rho, 4)
        x_sat += x_err
        y_sat += y_err
        z_sat += z_err
    # print(x_sat / RT)
    # print(y_sat / RT)
    # print(z_sat / RT)
    r_x, r_y, r_z, r_t = 0., 0., 0, 0.

    iterating, cnt = True, 0

    while iterating and cnt < max_iteration:
        try:
            # print('receptor position', f'{r_x = :.3e}, {r_y:.3e}, {r_z:.3e}, {r_t:.3e}')
            r = ((x_sat - r_x) ** 2 + (y_sat - r_y) ** 2 + (z_sat - r_z) ** 2) ** .5
            # print(f'{r = }')
            ax = (x_sat - r_x) / r
            ay = (y_sat - r_y) / r
            az = (z_sat - r_z) / r

            H = np.array([
                [ax[0], ay[0], az[0], 1.],
                [ax[1], ay[1], az[1], 1.],
                [ax[2], ay[2], az[2], 1.],
                [ax[3], ay[3], az[3], 1.]
            ])
            H_1 = np.linalg.inv(H)
            d_rho = r + r_t - np.array((rho1, rho2, rho3, rho4))
            # print(f'{d_rho = }')
            dx = H_1 @ d_rho
            # dx = np.einsum('ik,k->i', H_1, d_rho)
            # print(f'{dx = }')
            r_x, r_y, r_z, r_t = dx * (1, 1, 1, -1) + (r_x, r_y, r_z, r_t)
            iterating = np.sum(dx ** 2) ** .5 > epsilon
            cnt += 1
        except Exception:
            iterating = False
    # print('Final receptor position', f'{r_x = :.3e}, {r_y:.3e}, {r_z:.3e}, {r_t/LIGHT_SPEED:.3e}')
    # err = np.array((r_x, r_y, r_z, r_t)) - real_position * np.array((1., 1., 1., LIGHT_SPEED))
    # print(f'Error: {sum(err ** 2) ** .5:.3e}, {sum(err[:3] ** 2) ** .5 * 1e-3:.3e} km, {abs(err[3]) / LIGHT_SPEED:.3e} s')
    r = (r_x ** 2 + r_y ** 2 + r_z ** 2) ** .5
    # print(f'{r / RT= }')
    r_phi = np.arctan2(r_x, r_y)
    r_theta = np.arccos(r_z / r)
    # r_phi = np.arccos(r_x / r / np.sin(r_theta)) * (2 * (r_y > 0) - 1)
    return r_phi, r_theta, r - RT, r_t / LIGHT_SPEED


def solve_position_any_sat(*phi_theta_rho_sat, epsilon=1.e-6, real_position=(0, 0, RT, 0)):
    # shape: (n, 3)
    phi_theta_rho_sat = np.array(phi_theta_rho_sat)
    phi_sat, theta_sat, rho = phi_theta_rho_sat[:, 0], phi_theta_rho_sat[:, 1], phi_theta_rho_sat[:, 2]

    # shape: (n,)
    x_sat = SAT_DISTANCE * np.cos(phi_sat) * np.sin(theta_sat)
    y_sat = SAT_DISTANCE * np.sin(phi_sat) * np.sin(theta_sat)
    z_sat = SAT_DISTANCE * np.cos(theta_sat)
    at = np.ones(x_sat.shape, float)
    r_x, r_y, r_z, r_t = 0., 0., 0, 0.

    iterating = True

    while iterating:
        try:
            # print('receptor position', f'{r_x = :.3e}, {r_y:.3e}, {r_z:.3e}, {r_t:.3e}')
            # shape : (n,)
            r = ((x_sat - r_x) ** 2 + (y_sat - r_y) ** 2 + (z_sat - r_z) ** 2) ** .5
            # print(f'{r = }')
            # shape : (n,)
            ax = (x_sat - r_x) / r
            ay = (y_sat - r_y) / r
            az = (z_sat - r_z) / r

            # shape : (n, 4)
            H = np.concatenate(
                (
                    # shape : (n, 1)
                    ax[:, None],
                    ay[:, None],
                    az[:, None],
                    at[:, None]
                ), 1
            )
            H_T = H.transpose()
            Q = np.linalg.inv(H_T @ H)

            d_rho = r + r_t - rho
            dx = Q @ (H_T @ d_rho)
            r_x, r_y, r_z, r_t = dx * (1, 1, 1, -1) + (r_x, r_y, r_z, r_t)
            iterating = np.sum(dx ** 2) ** .5 > epsilon
        except Exception:
            print('Inner exception')
            iterating = False
    print('Final receptor position', f'{r_x = :.3e}, {r_y:.3e}, {r_z:.3e}, {r_t/LIGHT_SPEED:.3e}')
    err = np.array((r_x, r_y, r_z, r_t)) - real_position * np.array((1., 1., 1., LIGHT_SPEED))
    print(f'Error: {sum(err ** 2) ** .5:.3e}, {sum(err[:3] ** 2) ** .5 * 1e-3:.3e} km, {abs(err[3]) / LIGHT_SPEED:.3e} s')
    r = (r_x ** 2 + r_y ** 2 + r_z ** 2) ** .5
    print(f'{r / RT= }')
    r_phi = np.arctan2(r_x, r_y)
    r_theta = np.arccos(r_z / r)
    # r_phi = np.arccos(r_x / r / np.sin(r_theta)) * (2 * (r_y > 0) - 1)
    return r_phi, r_theta, r - RT, r_t / LIGHT_SPEED


def random_visible_satellite(rng):
    theta = np.arccos(1 - (1 - COS_TH_MAX) * rng.random())
    phi = 2 * np.pi * rng.random()
    return phi, theta
    # return SAT_DISTANCE * np.array([cos(phi) * sin(theta), sin(phi) * sin(theta), cos(theta)])


def random_spherical_point(rng, rho=1., num_points=1):
    theta = np.arccos(1 - 2 * rng.random(num_points))
    phi = 2 * np.pi * rng.random(num_points)
    return np.array(rho) * (np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta))


def spheric_to_cartesian(phi, theta, rho):
    return rho * np.array((cos(phi) * sin(theta), sin(phi) * sin(theta), cos(theta)))


def make_distances(*satellites, dt=0.):
    sat_arr = np.array(satellites)
    phi, theta = sat_arr[:, 0], sat_arr[:, 1]

    # shape: (n, 3)
    sat_pos = SAT_DISTANCE * np.array(
        [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]
    ).transpose()
    # print(f'{sat_pos / RT = }')
    # print((np.sum((sat_pos - np.array((0., 0., RT))[None, :]) ** 2, axis=1) ** .5 + LIGHT_SPEED * dt) * 1e-6)
    return np.sum((sat_pos - np.array((0., 0., RT))[None, :]) ** 2, axis=1) ** .5 + LIGHT_SPEED * dt


def test_4sat():
    rng = np.random.default_rng()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_aspect("equal")
    ax.set_box_aspect([1, 1, 1])
    set_axes_equal(ax)
    ax.set_axis_off()
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    s1, s2, s3, s4 = [random_visible_satellite(rng) for _ in range(4)]
    r1, r2, r3, r4 = make_distances(s1, s2, s3, s4, dt=0.)
    try:
        r_phi, r_theta, r_alt, dt = solve_receptor_position(rng, s1, s2, s3, s4, r1, r2, r3, r4)
        placepoint(spheric_to_cartesian(r_phi, r_theta, r_alt + RT + 1e3) / RT, ax, 'Red')
    except Exception as e:
        print(e)
    for sat in s1, s2, s3, s4:
        # print('sats : ', spheric_to_cartesian(*sat, SAT_DISTANCE / RT))
        placepoint(spheric_to_cartesian(*sat, SAT_DISTANCE / RT), ax)
    placepoint([0, 0, 1.01], ax)
    plt.show()


def test_q11():
    rng = np.random.default_rng()
    theta = np.arccos(COS_TH_MAX)
    th = theta * .5
    print(90. - np.arctan(SAT_DISTANCE * np.sin(theta * .5) / (SAT_DISTANCE * np.cos(theta * .5) - RT)) * 180 / np.pi)

    s1 = 3 * np.pi * .25, th
    s2 = 0, 0
    s3 = -3 * np.pi * .25, th
    s4 = 0, th
    r1, r2, r3, r4 = make_distances(s1, s2, s3, s4, dt=0.)

    xy_err = []
    rho_err = []
    t_err = []

    _theta = np.linspace(theta - 1e-7, 0, 1000, endpoint=False)
    elevation = 90. - np.arctan(SAT_DISTANCE * np.sin(_theta) / (SAT_DISTANCE * np.cos(_theta) - RT)) * 180 / np.pi

    n = 200
    rhos = np.linspace(0, 20, 100)
    for rho in rhos:
        _xy = 0.
        _rho = 0.
        _t = 0.
        # if abs(th - theta * .5) < 1e-3:
        #     xy_err.append(np.nan)
        #     rho_err.append(np.nan)
        #     t_err.append(np.nan)
        #     continue
        for _ in range(n):
            r_phi, r_theta, r_alt, dt = solve_receptor_position(rng, s1, s2, s3, s4, r1, r2, r3, r4, rho=rho, use_err=True)
            _xy += (RT + r_alt) * np.sin(r_theta)
            _rho += abs(r_alt)
            _t += abs(dt)
        xy_err.append(_xy / n)
        rho_err.append(_rho / n)
        t_err.append(_t / n)
    fig, ax = plt.subplots(1, 3)
    ax[0].plot(rhos, xy_err, color='b')
    ax[0].set_xlabel('Rayon erreur (m)')
    ax[0].set_ylabel('Erreur 2D (m)')
    ax[1].plot(rhos, rho_err, color='r')
    ax[1].set_xlabel('Rayon erreur (m)')
    ax[1].set_ylabel('Erreur d\'altitude (m)')
    ax[2].plot(rhos, t_err, color='g')
    ax[2].set_xlabel('Rayon erreur (m)')
    ax[2].set_ylabel('Erreur d\'horloge (s)')
    plt.show()


def test_any_sat(n):
    rng = np.random.default_rng()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_aspect("equal")
    ax.set_box_aspect([1, 1, 1])
    set_axes_equal(ax)
    ax.set_axis_off()
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
    satellites = [random_visible_satellite(rng) for _ in range(n)]
    distances = make_distances(*satellites, dt=0.)
    try:
        print(satellites, distances[:, None], sep='\n')
        phy_theta_rho = np.concatenate((satellites, distances[:, None]), axis=1)
        print(phy_theta_rho)
        r_phi, r_theta, r_alt, dt = solve_position_any_sat(*phy_theta_rho)
        placepoint(spheric_to_cartesian(r_phi, r_theta, r_alt + RT + 1e3) / RT, ax, 'Red')
    except Exception as e:
        print('Main exception')
        raise e from e
    for sat in satellites:
        # print('sats : ', spheric_to_cartesian(*sat, SAT_DISTANCE / RT))
        placepoint(spheric_to_cartesian(*sat, SAT_DISTANCE / RT), ax)
    placepoint([0, 0, 1.01], ax)
    plt.show()


if __name__ == '__main__':
    # test_any_sat(7)
    test_q11()