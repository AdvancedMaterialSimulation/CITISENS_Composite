
import numpy as np
import gmsh

def CircRect(x0, y0, z0, Lx, Ly,vec_z, vec_x, x_eps=1e-6):

    vec_z = vec_z / np.linalg.norm(vec_z)
    vec_x = vec_x / np.linalg.norm(vec_x)


    vec_y = np.cross(vec_z, vec_x)
    vec_y = vec_y / np.linalg.norm(vec_y)

    vec_x = np.cross(vec_y, vec_z)
    vec_x = vec_x / np.linalg.norm(vec_x)

    p1 = np.array([-Lx/2, 0, 0])
    p2 = np.array([+Lx/2, 0, 0])

    p1y1 = np.array([-Lx/2 - x_eps, +Ly, 0])
    p1y2 = np.array([-Lx/2 - x_eps, -Ly, 0])

    p2y1 = np.array([Lx/2 + x_eps, +Ly, 0])
    p2y2 = np.array([Lx/2 + x_eps, -Ly, 0])

    rot = np.column_stack((vec_x, vec_y, vec_z))

    p1 = np.dot(rot, p1)
    p2 = np.dot(rot, p2)

    p1y1 = np.dot(rot, p1y1)
    p1y2 = np.dot(rot, p1y2)

    p2y1 = np.dot(rot, p2y1)
    p2y2 = np.dot(rot, p2y2)

    # translate to the origin   
    p1 = p1 + np.array([x0, y0, z0])
    p2 = p2 + np.array([x0, y0, z0])

    p1y1 = p1y1 + np.array([x0, y0, z0])
    p1y2 = p1y2 + np.array([x0, y0, z0])

    p2y1 = p2y1 + np.array([x0, y0, z0])
    p2y2 = p2y2 + np.array([x0, y0, z0])

    p1 = gmsh.model.occ.addPoint(*p1)
    p1y1 = gmsh.model.occ.addPoint(*p1y1)
    p1y2 = gmsh.model.occ.addPoint(*p1y2)
    gmsh.model.occ.synchronize()


    p2 = gmsh.model.occ.addPoint(*p2)
    p2y1 = gmsh.model.occ.addPoint(*p2y1)
    p2y2 = gmsh.model.occ.addPoint(*p2y2)
    gmsh.model.occ.synchronize()

    arc1 = gmsh.model.occ.addCircleArc(p1y1, p1, p1y2)
    ly2  = gmsh.model.occ.addLine(p1y2,p2y2)

    arc2 = gmsh.model.occ.addCircleArc(p2y2, p2,p2y1)
    ly1  = gmsh.model.occ.addLine(p2y1,p1y1)

    # create the surface
    curve_loop = gmsh.model.occ.addCurveLoop([arc1, ly2, arc2, ly1])

    # cerrar curve 

    # wire1 = gmsh.model.occ.addWire([curve_loop],checkClosed=True)

    ss = gmsh.model.occ.addPlaneSurface([curve_loop])

    gmsh.model.occ.synchronize()

    return curve_loop
