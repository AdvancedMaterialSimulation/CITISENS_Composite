import gmsh 
import numpy as np
import os 
from CompositeSandwich.box_labeling import box_labeling
join = os.path.join

def CreateGeoBending(params):


    t_n = params["t_n"]
    t_l = params["t_l"]
    Lx = params["Lx"]
    Ly = params["Ly"]
    n_l = params["n_l"]
    output = params["output_folder"]
    meshsizefactor = params["meshsizefactor"]

    t_t = 2*t_l*n_l + t_n
    params["t_t"] = t_t
    # Create a box layers 
    gmsh.initialize()

    gmsh.model.add("compisite_Layers")
    # create a fullbox 

    addBox = lambda Lz: gmsh.model.occ.addBox( 0  ,  0  , -Lz/2, 
                                                Lx ,  Ly , Lz)
    total_box  = addBox(t_t)
    gmsh.model.occ.synchronize()


    # add planes 
    zspan = [2*t_l*i + t_n for i in range(0,n_l,1)] 
    zspan = np.array(zspan)/2
    zspan = np.concatenate((-zspan, zspan))

    wires = []
    for z in zspan:
        wireTag = gmsh.model.occ.addRectangle(0, 0, z, Lx, Ly)
        wires.append(wireTag)
    gmsh.model.occ.synchronize()

    # fragment the box
    gmsh.model.occ.fragment([(3, total_box)], [(2, wire) for wire in wires])

    gmsh.model.occ.synchronize()


    volumen = gmsh.model.getEntities(3)
    # sort by z 
    center_z = np.array([gmsh.model.occ.getCenterOfMass(3, vol[1])[2] for vol in volumen])
    idx = np.argsort(center_z)
    volumen = np.array(volumen)[idx]

    names = ["Layer_{}".format(abs(i))
            for i in range(-n_l,n_l+1)]
    sign = [ "plus" if i > 0 else "minus" for i in range(-n_l,n_l+1)]

    names = [name + "_" + s for name,s in zip(names,sign)]
    names
    # the element that cotain layer 0 replace by nucleo
    names[n_l] = "nucleo"

    # add physical group
    for name, vol in zip(names, volumen):
        gmsh.model.addPhysicalGroup(3, [vol[1]],name= name)

    # select all surface which center of mass is in the plane x = 0
    # ============================================================
    surfaces = gmsh.model.getEntities(2)
    surfaces = np.array(surfaces)
    center_x = np.array([gmsh.model.occ.getCenterOfMass(2, surf[1])[0] for surf in surfaces])

    idx = np.where(center_x == 0)[0]

    # add physical group
    gmsh.model.addPhysicalGroup(2, [surf[1] for surf in surfaces[idx]], name = "symmetry")

    # select all egdes which center of mass is in x = Lx and z=0

    edges = gmsh.model.getEntities(1)
    edges = np.array(edges)
    center_x = np.array([gmsh.model.occ.getCenterOfMass(1, edge[1])[0] for edge in edges])
    center_z = np.array([gmsh.model.occ.getCenterOfMass(1, edge[1])[2] for edge in edges])

    idx = np.where((center_x == Lx) & (center_z == 0))[0]

    # add physical group

    gmsh.model.occ.synchronize()

    # 
    volumens = gmsh.model.getEntities(3)
    # sort volumens by z
    center_z = np.array([gmsh.model.occ.getCenterOfMass(3, vol[1])[2] for vol in volumens])
    idx = np.argsort(center_z)
    volumens = np.array(volumens)[idx]
    for i,vol in enumerate(volumens):
        box_labeling(vol[1],str("Layer_{}".format(i)))

    # set size 0.1 of Characteristic Length min
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.01)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 6*t_l*meshsizefactor)

    #
    field = gmsh.model.mesh.field
    field.add("MathEval", 1)
    field.setString(1, "F", "0.5 + 1.7 * Abs(x)")  # Más refinado cerca de x=0
    
    #field.setString(1, "F", "0.5 + 1.7 * Abs(x)")  # Más refinado cerca de x=0
    #field.setString(1, "F", "0.5 + 1.1 * Abs(x) + 1.1 * (Abs(z) > 1.5 ? 1 : 0)")

    # Aplicar el campo de fondo
    field.setAsBackgroundMesh(1)
    # mesh 
    # near to the symmetry plane, the mesh is finer


    # set the point of the symmetry plane

    #
    gmsh.model.mesh.generate(3)
    # save inp 
    # set order 
    gmsh.model.mesh.setOrder(2)
    gmsh.write(join(output,"composite_layers.inp"))
    #final 
    gmsh.finalize()
