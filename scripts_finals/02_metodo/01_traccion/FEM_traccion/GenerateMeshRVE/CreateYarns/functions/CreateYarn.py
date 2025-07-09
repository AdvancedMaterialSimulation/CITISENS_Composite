import gmsh
import numpy as np
from .reduce_points import reduce_points
from gmshtools.CircRect6 import CircRect

# =============================================================================


def addProfile(x, y, z, rx, ry, vec_z, vec_x):  

    profile_tag = CircRect(x, y, z, rx, ry, vec_z, vec_x)
    return profile_tag
    
# =============================================================================


def CreateYarn(params):

    plausible_final =np.array([[1,0,0], [0,1,0], [-1,0,0], [0,-1,0] ] )

    trajs  = params["trajs"]
    file   = params["file"]
    radius = params["radius"]
    d       = params["d"]

    rx = radius 
    ry = d 

    density = params["density"] 
    trajs,trajs_vec = reduce_points(trajs, radius,density=density)

    first_vector_computed = trajs_vec[0].copy()
    first_vector_computed = first_vector_computed / np.linalg.norm(first_vector_computed)
    last_vector_computed  = trajs_vec[-1].copy()
    last_vector_computed = last_vector_computed / np.linalg.norm(last_vector_computed)

    distance_to_plausible = lambda x: np.linalg.norm(x - plausible_final, axis=1)

    # get the plausible vector
    last_vector = trajs_vec[-1]
    last_vector = last_vector / np.linalg.norm(last_vector)
    last_vector = plausible_final[np.argmin(distance_to_plausible(last_vector))].copy()

    trajs_vec[-1] = last_vector


    # first vector
    first_vector = trajs_vec[0]
    first_vector = first_vector / np.linalg.norm(first_vector)
    first_vector = plausible_final[np.argmin(distance_to_plausible(first_vector))].copy()
    trajs_vec[0] = first_vector
    # 
    # Iniciar GMSH
    gmsh.initialize()
    # verbose 0 
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.clear()

    gmsh.option.setNumber("Geometry.Tolerance", 1e-5)  # Ajusta la tolerancia
    #verbose of 
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.Verbosity", 0)


    gmsh.model.add("Fourier_Cylinder_OCC_Pipe")

    # Parámetros de la trayectoria
    # given x,y,z, r
    # add disk 

    id = 0
    disks = []
    wires = []

    # first angle 


    # first disk can be a ellipse 
    x, y, z = trajs[0]

    xAxis = np.cross(trajs_vec[0], [0,0,1])

    disk = addProfile(x, y, z,
                      rx, ry,
                      trajs_vec[0], 
                      xAxis)
    
    wires.append(gmsh.model.occ.addWire([disk]))
    
    disks.append(disk)
    id += 1
    
    for i in range(1,len(trajs)-1):
        x, y, z = trajs[i]

        # xAxis is trajs_vec[i] and  z = [0,0,1]
        xAxis = np.cross(trajs_vec[i], [0,0,1])
        
        disk = addProfile(x, y, z,
                    rx, ry,
                    trajs_vec[i], 
                    xAxis)
        # crear loop from disk
        wires.append(gmsh.model.occ.addWire([disk]))
        disks.append(disk)
        id += 1

    # last disk
    x, y, z = trajs[-1]

    xAxis = np.cross(trajs_vec[-1], [0,0,1])
    disk = addProfile(x, y, z,
                    rx, ry,
                    trajs_vec[-1], 
                    xAxis)
    
    
    disks.append(disk)
    wires.append(gmsh.model.occ.addWire([disk]))
    id += 1

    gmsh.model.occ.synchronize()
    # addThruSections
    volumes = []
    for i in range(len(disks)-1):
        v = gmsh.model.occ.addThruSections([disks[i], disks[i+1]],
                                           makeSolid=True)
        volumes.append(v)


    for i in range(10000):
        volumes = gmsh.model.occ.getEntities(3)
        try:
            gmsh.model.occ.fuse([volumes[-1]],
                                [volumes[-2]],
                                removeObject=True,
                                removeTool=True)
        except:
            break
        gmsh.model.occ.synchronize()

    # save geometry

    gmsh.model.occ.synchronize()

    gmsh.write(file) 
    # Finalizar GMSH
    gmsh.finalize()