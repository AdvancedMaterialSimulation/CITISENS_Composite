import gmsh
import glob
import os
import numpy as np
from CompositeSandwich.box_labeling import box_labeling
from .SetNames import SetNames
from ..inp.are_coplanar import are_coplanar



def CreateBoxMirror(params_yarns,output_folder):


    Lx = params_yarns["Lx"]
    Ly = params_yarns["Ly"]
    h = params_yarns["h"]
    # z0 = 2*(params_yarns["z0"] - 0.5*h)
    
    z0 = 2*(params_yarns["z0"])

    zL = h*(len(params_yarns["trajs_layers"]))*2 
    zT = z0 + zL
    radius = params_yarns["r"]

    # load all the geometries
    files_yarns = glob.glob(os.path.join(*output_folder,"*.brep"))

    # ==================================================
    # Set names and sort
    names,files_yarns = SetNames(files_yarns)

    # select layer_1 
    files_yarns = [i for i in files_yarns if "plus" in i]
    names = [i for i in names if "PL" in i]
    # select 
    # ==================================================

    gmsh.initialize()
    gmsh.clear()



    fc_mesh_min = params_yarns["fc_mesh_min"]
    fc_mesh_max = params_yarns["fc_mesh_max"]




    # gmsh.option.setNumber("Geometry.Tolerance", 1e-5)

    if len(gmsh.model.getEntities()) != 0:
        raise ValueError("The model is not empty")

    yarns_vols = []
    yarns_surfaces = []

    yarns_dict = {}
    for name,file in zip(names,files_yarns):
        gmsh.merge(file)
        gmsh.model.occ.synchronize()

        all_vols = gmsh.model.getEntities(3)
        all_surfaces = gmsh.model.getEntities(2)
        new_vols     = [i for i in all_vols if i not in yarns_vols]
        new_surfaces = [i for i in all_surfaces if i not in yarns_surfaces]
        
        yarns_dict[name] = new_vols
        yarns_vols += new_vols
        
        if params_yarns["with_interface"]:
            gmsh.model.addPhysicalGroup(3, [new_vols[1][1]] , tag=-1,name=name+"_interface")

            #take the points of the interface
            surfaces_interface =  gmsh.model.getBoundary(new_vols[:1], recursive=True)
            gmsh.model.mesh.setSize(surfaces_interface, fc_mesh_min*radius)
            # gmsh.model.mesh.setRecombine(2, new_vols[1][1],angle=90)
            # gmsh.model.mesh.setRecombine(2, new_vols[0][1],angle=90)
            
            gmsh.model.addPhysicalGroup(3, [new_vols[0][1]] , tag=-1,name=name+"_yarn")


        else:
            gmsh.model.addPhysicalGroup(3, [new_vols[0][1]] , tag=-1,name=name+"_yarn")
            # surface boundary
            surfaces_interface =  gmsh.model.getBoundary(new_vols[:1])
            surfaces_interface = [ (dim,abs(tag)) for dim,tag in surfaces_interface]

            # len of points 
            
            gmsh.model.occ.synchronize()

            points = [ gmsh.model.getBoundary([isurf], recursive=True) for isurf in surfaces_interface]

            len_points = [ len(ipoint) for ipoint in points]

            points_mu = [ gmsh.model.occ.getCenterOfMass(2, isurf[1]) for isurf in surfaces_interface]
            points_coord = [ [gmsh.model.getValue(0,i[1],[]) for i in ipoint] for ipoint in points]
            # add the point mu to the points_coord
            points_coord = [ [imu] + ipoint for imu,ipoint in zip(points_mu,points_coord)]

            interface_bool = [not are_coplanar(ipoint) for ipoint in points_coord]

            surfaces_interface_selected = [isurf for isurf,ibool in zip(surfaces_interface,interface_bool) if ibool]

            if len(surfaces_interface_selected) == 0:
                surfaces_interface_selected = [isurf for isurf,ilen in zip(surfaces_interface,len_points) if ilen == 2]

            gmsh.model.addPhysicalGroup(2, [i[1] for i in surfaces_interface_selected], tag=-1,name=name+"_interface")


    gmsh.model.occ.synchronize()
    yarns_vols = gmsh.model.getEntities(3)

    # box 


    if params_yarns["z0"] != 0:
        big_box = gmsh.model.occ.addBox(0, 0, 0, 
                        Lx, Ly,zT/2)

        mid_box = gmsh.model.occ.addBox(0 , 0 , 0, 
                            Lx, Ly, z0/2)
        
        # cut the box 
        gmsh.model.occ.cut([(3, big_box)], [(3, mid_box)], removeTool=False)

    else:
        big_box = gmsh.model.occ.addBox(0, 0, -h/2, 
                        Lx, Ly,h)
        
    gmsh.model.occ.synchronize()

    #gmsh.fltk.run()



    box_vols = gmsh.model.getEntities(3)
    box_vols = [i for i in box_vols if i not in yarns_vols]


    final_obj_box = gmsh.model.occ.cut(box_vols, yarns_vols, removeTool=False)
    # gmsh.fltk.run()

    # cut the yarns 
    final_obj_box = final_obj_box[0]
    #center of mass 
    gmsh.model.occ.synchronize()    


    COM = [ gmsh.model.occ.getCenterOfMass(3, ibox[1]) for ibox in final_obj_box]
    # sort by z
    id_com = sorted(range(len(COM)), key=lambda k: COM[k][2])
    final_obj_box = [final_obj_box[i] for i in id_com]

    if params_yarns["z0"] != 0: 
        names_box = ["alma","box_plus"]
    else:
        names_box = ["box_plus"]

    for name, ibox in zip(names_box,final_obj_box):
        gmsh.model.addPhysicalGroup(3, [ibox[1]], tag=-1,name=name)


    gmsh.model.occ.synchronize()

    if params_yarns["z0"] != 0:
        box_labeling(final_obj_box[0][1],"alma")
        box_labeling(final_obj_box[1][1],"plus")
    else:
        box_labeling(final_obj_box[0][1],"plus")

    #get all surface cuyo centro de mass este en el plano x=0
    all_surfaces = gmsh.model.getEntities(2)

    # get the center of mass of the surfaces
    COM = [ gmsh.model.occ.getCenterOfMass(2, isurf[1]) for isurf in all_surfaces]

    # tol 
    COM = [ [round(i,1) for i in icom] for icom in COM]
    planes = [
        ("x0_plane", 0, 1e-6, 0),  # (name, index to check, tolerance, offset)
        ("y0_plane", 1, 1e-6, 0),
        ("xL_plane", 0, 1e-6, Lx),
        ("yL_plane", 1, 1e-6, Ly)
    ]

    # Iterar sobre cada plano especificado
    surfaces_limits = []
    for name, idx, tol, offset in planes:
        # Seleccionar superficies que están cerca del plano definido
        id_com = [i for i, com in enumerate(COM) if abs(com[idx] - offset) < tol]
        surfaces_limits.append(id_com)
        
        # Añadir grupo físico con las superficies seleccionadas
        gmsh.model.addPhysicalGroup(2, [all_surfaces[i][1] for i in id_com], tag=-1, name=name)



    # 1) Eliminar entidades duplicadas
    gmsh.model.occ.removeAllDuplicates()
    
    # write .brep 
    gmsh.model.occ.synchronize()
    gmsh.write(os.path.join(*output_folder,"composite.brep"))
    print("Meshing ... ")

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", radius*fc_mesh_min)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", radius*fc_mesh_max)

    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature",25) # 20
    # gmsh.option.setNumber("Mesh.MeshSizeFromCurvatureIsotropic",1) # True
    gmsh.option.setNumber("Mesh.Algorithm", 2)
    # gmsh.option.setNumber("Mesh.Algorithm3D", 2)

    # gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 1)
    # gmsh.option.setNumber("Mesh.Optimize", 1)
    # gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)
    # gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
    # gmsh.option.setNumber("Mesh.Smoothing", 10)


    try:
        gmsh.model.mesh.generate(3)
    except Exception as e:
        print("Error: ",e)
        gmsh.fltk.run()



    print("Optimizing mesh ... ")
    gmsh.model.mesh.setOrder(2)
    #gmsh.write(os.path.join(*output_folder,"composite_pre.inp"))

    gmsh.model.mesh.optimize("HighOrderElastic",niter=10)  # Prueba con Netgen u otro método

    #recombine
    # gmsh.model.mesh.recombine()
    # Agregar un campo de tipo "Box"

    # inp 
    gmsh.write(os.path.join(*output_folder,"composite.inp"))

    gmsh.finalize()


    return params_yarns