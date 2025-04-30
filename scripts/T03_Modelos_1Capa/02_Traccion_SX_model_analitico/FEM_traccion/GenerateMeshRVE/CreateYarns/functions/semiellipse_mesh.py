import numpy as np
import gmsh
from gmshtools.CircRect6 import CircRect

addProfile = gmsh.model.occ.addDisk
addProfile = CircRect

def semiellipse_mesh(itraj,radius,file,d):
    
    r0 = itraj[0]
    vec = itraj[-1] - r0
    vec_norm = vec/np.linalg.norm(vec)

    direction = "x" if vec_norm[0] != 0 else "y"

    if direction == "y":
        shift = r0[0]
    else:
        shift = r0[1]

    radius_x = radius
    radius_y = d

    h = np.linalg.norm(vec)

    b = 1 if shift == 0 else 0

    zy = r0[2]


    if direction =="x":
        direction_vec = [1,0,0]
        xAxis = [0,1,0]
    elif direction =="y":
        direction_vec = [0,1,0]
        xAxis = [1,0,0]

    gmsh.initialize()
    gmsh.clear()
    gmsh.model.add("half_ellipse")

    # Parámetros de la elipse
    x, y, z = 0, 0, 0  # Centro de la elipse
    # Crear la elipse completa
    x2 = x + direction_vec[0]*h
    y2 = y + direction_vec[1]*h
    z2 = z + direction_vec[2]*h
    elipse_surface_1 = addProfile(x, y, z   , radius_x, radius_y , direction_vec,xAxis)
    elipse_surface_2 = addProfile(x2, y2, z2, radius_x, radius_y , direction_vec,xAxis)


    gmsh.model.occ.synchronize()

    # pipe 
    # Crear el cilindro
    cylinder = gmsh.model.occ.addThruSections([elipse_surface_1, elipse_surface_2])
    gmsh.model.occ.synchronize()

    # plane
    # Crear el plano
    if direction == "x":
        plane = gmsh.model.occ.addRectangle(0, -radius_y, 0, h, 2*radius_y)
        gmsh.model.occ.rotate([(2, plane)], x, y, z, 1, 0, 0, np.pi/2)

        if b == 0:
            gmsh.model.occ.rotate(cylinder, x, y, z, 1, 0, 0, np.pi)

    elif direction == "y":
        plane = gmsh.model.occ.addRectangle(-radius_y, 0, 0, 2*radius_y, h)
        gmsh.model.occ.rotate([(2, plane)], x, y, z, 0, 1, 0, np.pi/2)

        if b == 0:
            gmsh.model.occ.rotate( cylinder, x, y, z, 0, 1, 0, np.pi)

    gmsh.model.occ.synchronize()
    #
    # rotate 
    # Rotar el plano
    #
    gmsh.model.occ.synchronize()

    # fragment
    # Fragmentar el cilindro con el plano

    fragment = gmsh.model.occ.fragment(cylinder, [(2, plane)], removeObject=True)


    # gmsh.fltk.run()
    semicylinders = fragment[1][0]

    # remove semicylinders
    gmsh.model.occ.remove([semicylinders[0]])

    # remove all surfaces 
    gmsh.model.occ.synchronize()

    surfaces = gmsh.model.getEntities(2)
    gmsh.model.occ.remove(surfaces)
    gmsh.model.occ.synchronize()
    
    volumes = gmsh.model.getEntities(3)

    # tranlate 
    if direction == "x":
        gmsh.model.occ.translate(volumes, 0, shift, zy)
    elif direction == "y":
        gmsh.model.occ.translate(volumes, shift, 0, zy)


    gmsh.model.occ.synchronize()


    # gmsh.fltk.run()
    #write inp 
    
    # mesh 
    # gmsh.option.setNumber("Mesh.MeshSizeFromCurvature",25) # 20
    # gmsh.model.mesh.generate(3)
    gmsh.model.occ.synchronize()

    gmsh.write(file)