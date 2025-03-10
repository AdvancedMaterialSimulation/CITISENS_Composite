import gmsh
import numpy as np
from .semielipse import semielipse
def semiellipse_mesh(itraj,radius,file,factor_radius):
    
    r0 = itraj[0]
    vec = itraj[-1] - r0
    vec_norm = vec/np.linalg.norm(vec)

    dir = "x" if vec_norm[0] != 0 else "y"

    if dir == "y":
        shift = r0[0]
    else:
        shift = r0[1]

    

    radius_x = radius*factor_radius
    radius_y = radius/factor_radius

    h = np.linalg.norm(vec)

    b = 1 if shift == 0 else 0

    z = r0[2]

    semielipse(dir,radius_x,radius_y,h,b,shift,file,z)
