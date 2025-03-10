import gmsh
import numpy as np

def semielipse(direction,radius_x,radius_y,h,b,shift,file,zy):

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
    elipse_surface_1 = gmsh.model.occ.addDisk(x, y, z, radius_x, radius_y  , xAxis=xAxis,zAxis=direction_vec)
    elipse_surface_2 = gmsh.model.occ.addDisk(x2, y2, z2, radius_x, radius_y, xAxis=xAxis,zAxis=direction_vec)


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
    gmsh.model.occ.remove([semicylinders[1]])

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