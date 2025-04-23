import gmsh
import numpy as np
from gmshtools.CircRect6 import CircRect
from gmshtools.ElipseRect6 import ElipseRect
from gmshtools.reduce_points import reduce_points


def CreateYarnRect(params):

    volumes_old  = gmsh.model.occ.getEntities(3)
    volumes_old  = [v[1] for v in volumes_old]

    surfaces_old = gmsh.model.occ.getEntities(2)
    surfaces_old = [s[1] for s in surfaces_old]

    lines_old = gmsh.model.occ.getEntities(1)
    lines_old = [l[1] for l in lines_old]

    points_old = gmsh.model.occ.getEntities(0)
    points_old = [p[1] for p in points_old]


    trajs  = params["trajs"]
    radius = params["radius"]
    vec_init = params["vec_init"]
    vec_end  = params["vec_end"]
    skip_left = params["skip_left"]
    skip_right = params["skip_right"]


    factor = 2.2
    rx = factor*radius
    ry = (1/factor)*radius

    density = params["density"] 
    trajs,trajs_vec = reduce_points(trajs,
                                    density=density,
                                    skip_left=skip_left,
                                    skip_right=skip_right)

    # angles between vectors
    angle_end = np.arccos(np.dot(vec_end, trajs_vec[-1] ) / (np.linalg.norm(vec_end)*np.linalg.norm(trajs_vec[-1])))
    factor_end = 1/np.cos(angle_end)

    angle_init = np.arccos(np.dot(vec_init, trajs_vec[0] ) / (np.linalg.norm(vec_init)*np.linalg.norm(trajs_vec[0])))
    factor_init = 1/np.cos(angle_init)


    trajs_vec[-1] = vec_end
    trajs_vec[0]  = vec_init

    # 
    id = 0
    disks = []

    # first disk can be a ellipse 
    x, y, z = trajs[0]

    xAxis = np.cross(trajs_vec[0], [0,0,1])

    ff = 1.2

    disk = CircRect(x, y, z,
                    ff*factor_init*rx, ry,
                    trajs_vec[0], xAxis)
    
    disks.append(disk)
    id += 1
    
    for i in range(1,len(trajs)-1):
        x, y, z = trajs[i]

        # xAxis is trajs_vec[i] and  z = [0,0,1]
        xAxis = np.cross(trajs_vec[i], [0,0,1])
        
        disk = CircRect(x, y, z, 
                        rx, ry, 
                        trajs_vec[i], xAxis)
        # crear loop from disk
        
        disks.append(disk)
        id += 1

    # last disk
    x, y, z = trajs[-1]

    xAxis = np.cross(trajs_vec[-1], [0,0,1])
    disk = CircRect(x, y, z,
                    ff*factor_end*rx, ry,
                    trajs_vec[-1], xAxis)
    
    
    disks.append(disk)
    id += 1

    gmsh.model.occ.synchronize()
    # addThruSections
    volumes = []
    for i in range(len(disks)-1):
        v = gmsh.model.occ.addThruSections([disks[i], disks[i+1]],
                                           makeSolid=True)
        volumes.append(v)

    gmsh.model.occ.synchronize()

    for i in range(10000):
        volumes = gmsh.model.occ.getEntities(3)
        volumes = [ v for v in volumes if v[1] not in volumes_old]
        try:
            gmsh.model.occ.fuse([volumes[-1]],
                                [volumes[-2]],
                                removeObject=True,
                                removeTool=True)
        except:
            break
        gmsh.model.occ.synchronize()

    gmsh.model.occ.synchronize()

    # select the new volume
    volumes = gmsh.model.occ.getEntities(3)
    volumes = [ v for v in volumes if v[1] not in volumes_old]

    surfaces = gmsh.model.occ.getEntities(2)
    surfaces = [ s for s in surfaces if s[1] not in surfaces_old]

    lines = gmsh.model.occ.getEntities(1)
    lines = [ l for l in lines if l[1] not in lines_old]

    points = gmsh.model.occ.getEntities(0)
    points = [ p for p in points if p[1] not in points_old]

    # remove surfaces

    remove_elements = False

    if remove_elements:
        gmsh.model.occ.remove(surfaces,recursive=True)
        gmsh.model.occ.synchronize()
        gmsh.model.occ.remove(lines,recursive=True)
        gmsh.model.occ.synchronize()
        gmsh.model.occ.remove(points,recursive=True)
        gmsh.model.occ.synchronize()

    return {"volumes":volumes}

   