import gmsh
import numpy as np
def semicylinder_mesh(itraj,radius,file):
    
    r0 = itraj[0]
    vec = itraj[-1] - r0
    vec_norm = vec/np.linalg.norm(vec)

    dir = "x" if vec_norm[0] != 0 else "y"

    if dir == "y":
        angle = 0 if r0[0] == 0 else np.pi
    else:
        angle = np.pi if r0[1] == 0 else 0

    gmsh.initialize()
    # verbose 0
    #clear
    gmsh.clear()
    #verbose 0
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add("composite")

    # circle 
    x  , y  , z  = r0
    dx , dy , dz = vec
    cyl = gmsh.model.occ.addCylinder(x , y  , z  , 
                            dx, dy , dz , 
                            radius,-1, angle = np.pi)
    
    vx = vec_norm[0]
    vy = vec_norm[1]
    vz = vec_norm[2]

    gmsh.model.occ.rotate([(3,cyl)],  x , y  , z,
                                     vx , vy ,vz, 
                                     angle)
                          
    gmsh.model.occ.synchronize()

    gmsh.write(file) 
    gmsh.finalize()