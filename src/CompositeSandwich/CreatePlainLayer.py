import numpy as np
import gmsh

def CreatePlainLayer(trajs, xlims, ylims, Lx, Ly, Lz, h_mid, radius):
    
    all_points = np.concatenate(trajs)

    # select the points have x = 0
    points = all_points[all_points[:,1] == 0]
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
        gmsh.model.setPhysicalName(3, ph, "cylinder_"+str(i+1))
