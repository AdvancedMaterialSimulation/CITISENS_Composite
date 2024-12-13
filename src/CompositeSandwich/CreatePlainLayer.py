import numpy as np
import gmsh
from .process_surfaces_in_plane import process_surfaces_in_plane

def CreatePlainLayer(trajs, xlims, ylims, Lx, Ly, Lz, h_mid, radius):
    
    pre_exist_surfaces = gmsh.model.getEntities(2)

    all_points = np.concatenate(trajs)

    # select the points have x = 0

    points = all_points[ np.abs(all_points[:,1] - 0) < 1e-3]
    new_points = []
    for i in range(1, len(points)):
        p1 = points[i-1]
        p2 = points[i]
        new_points.append( (p1 + p2)/2 )

    new_points = np.array(new_points)
    points = np.vstack([points, new_points])
    # sort the points
    points = points[np.argsort(points[:,0])]


    # add cilinder
    cylinders = []
    for i in range(len(points)):
        x = points[i,0]
        y = points[i,1]
        z = Lz+h_mid + Lz/2
        cyl = gmsh.model.occ.addCylinder(x, y, z, 0, Ly, 0, radius,-1)
        cylinders.append(cyl)

    # add semi-cylinder in init and end
    x = 0
    y = 0
    z = Lz+h_mid + Lz/2
    cyl = gmsh.model.occ.addCylinder(x, y, z, 0, Ly, 0, radius,-1, angle = np.pi)

    cylinders.append(cyl)

    x = Lx
    y = 0
    z = Lz+h_mid + Lz/2
    cyl = gmsh.model.occ.addCylinder(x, y, z, 0, Ly, 0, radius,-1, angle = np.pi)
    gmsh.model.occ.synchronize()
    # rotate 
    gmsh.model.occ.rotate([(3,cyl)], x, y, z,
                                        0, 1, 0, np.pi)

    cylinders.append(cyl)
        

    gmsh.model.occ.synchronize()

    # add box 
    box = gmsh.model.occ.addBox(xlims[0] , ylims[0] , Lz + h_mid ,
                                Lx       , Ly       , Lz)
    
    # cut 
    holow_box = gmsh.model.occ.cut([(3,box)], [(3,cyl) for cyl in cylinders],
                                    removeTool=False)

    gmsh.model.occ.synchronize()

    # add physical group
    #
    ph = gmsh.model.addPhysicalGroup(3,[holow_box[0][0][1]], -1)
    gmsh.model.setPhysicalName(3, ph, "box")

    # add physical group cylinders
    for i in range(len(cylinders)):
        ph = gmsh.model.addPhysicalGroup(3,[cylinders[i]], -1)
        gmsh.model.setPhysicalName(3, ph, "ly_2_yarn_"+str(i+1))


    gmsh.model.occ.synchronize()

    surfaces = []
    all_surfaces = gmsh.model.getEntities(2)
    all_surfaces = [i for i in all_surfaces if i not in pre_exist_surfaces]

    for surface in all_surfaces:
        surfaces.append( (surface, gmsh.model.occ.getCenterOfMass(2, surface[1])) )

    cases = [(0, 0,  'x',"0"), 
             (0, Lx, 'x',"L"), 
             (1, 0,  'y',"0"),
             (1, Ly, 'y',"L")]
    
    tags_split = []
    for coord, value, plane,name in cases:
        results = process_surfaces_in_plane(surfaces, coord, value, 
                                            "ly_2_", plane,name)
        
        tags_split.append({
            "cord" : coord,
            "value" : value,
            "plane" : plane,
            "name" : name,
            "results" : results
        })
    # add periodicity
    tx = -Lx
    ty = 0
    tz = 0

    transformation = [  1 ,0 ,0 ,tx ,
                        0 ,1 ,0 ,ty ,
                        0 ,0 ,1 ,tz ,
                        0 ,0 ,0 ,0]
    
    tags_min_x = [ i for i in tags_split if     i["plane"] == "x" 
                                            and i["value"] == 0 ][0]["results"]
    
    tags_max_x = [ i for i in tags_split if i["plane"] == "x" 
                                            and i["value"] == Lx][0]["results"]

 
    # sort 
    tags_max_x = sorted(tags_max_x["rectangle"], key=lambda x: gmsh.model.occ.getCenterOfMass(2,x)[2])
    tags_min_x = sorted(tags_min_x["rectangle"], key=lambda x: gmsh.model.occ.getCenterOfMass(2,x)[2])
 
    gmsh.model.mesh.setPeriodic(2,tags_min_x ,
                                  tags_max_x ,transformation)
 

    return holow_box, cylinders,tags_split