
import numpy as np

def LayerX(Lx=1,Ly=1, Nx=10):

    dx = Lx/Nx


    tspan = np.linspace(0,1,1000)

    trajs = []
    for i in range(Nx+1):
        x = i*dx + 0*tspan
        y = Ly*tspan    
        zl = np.zeros_like(x) 
        traj = np.vstack((x,y,zl)).T

        trajs.append(traj)
    
    return trajs

def LayerY(Lx=1,Ly=1, Ny=10):

    dy = Ly/Ny

    tspan = np.linspace(0,1,1000)

    trajs = []
    for i in range(Ny+1):
        y = i*dy + 0*tspan
        x = Lx*tspan    
        zl = np.zeros_like(y)
        traj = np.vstack((x,y,zl)).T

        trajs.append(traj)
    
    return trajs


