from CompositeSandwich.CombineTrajs import CombineTrajs
import numpy as np
from .base import sincos,circle,sincos_sm

def LayerSinY_smooth(Nx=2,Ny=2,type='sin',r=5):

    if type == 'sin':
        trajs = sincos_sm(r)
    elif type == 'circle':
        trajs = circle(r)
    else:
        raise ValueError('type must be sin or circle')

    
    # Datos iniciales
    Nx_base = 6
    Ny_base = 6
    all_points = np.concatenate(trajs)
    Lx = np.max(all_points[:, 0]) - np.min(all_points[:, 0])
    Ly = np.max(all_points[:, 1]) - np.min(all_points[:, 1])

    # Réplica de trayectorias
    all_trajs_1 = []
    for ix in range(Nx_base):
        for iy in range(Ny_base):
            for itraj in trajs:
                new_traj = np.copy(itraj)
                if ix % 2 == 1:
                    new_traj[:, 0] = -new_traj[:, 0] + Lx
                    # reverse
                    new_traj = new_traj[::-1]


                new_traj[:, 0] += ix * Lx
                new_traj[:, 1] += iy * Ly
                    
                all_trajs_1.append(new_traj)



    all_trajs_2 = []

    rot_z = np.pi/2
    matrix = np.array([[np.cos(rot_z), -np.sin(rot_z), 0],
                        [np.sin(rot_z), np.cos(rot_z), 0],
                        [0, 0, 1]])

    all_points = np.concatenate(all_trajs_1)
    xmu = np.mean(all_points[:, 0])
    ymu = np.mean(all_points[:, 1])

    for itraj in all_trajs_1:
        new_traj = np.copy(itraj)
        new_traj[:, 0] = itraj[:, 0] - xmu
        new_traj[:, 1] = itraj[:, 1] - ymu
        new_traj = np.dot(new_traj, matrix.T)
        new_traj[:, 0] += xmu
        new_traj[:, 1] += ymu
        

        all_trajs_2.append(new_traj)



    Nx_sel = Nx
    Ny_sel = Ny
    cond = lambda x,y: np.min(x) >= -1e2           and \
                    np.max(x) <= Nx_sel * Lx + 1e-2 and \
                    np.min(y) >= -1e-2           and \
                    np.max(y) <= Ny_sel * Ly + 1e-2

    all_trajs_2 = [itraj for itraj in all_trajs_2 
                   if cond(itraj[:, 0], itraj[:, 1])]

    trajs_2 = CombineTrajs(all_trajs_2)

    return trajs_2
