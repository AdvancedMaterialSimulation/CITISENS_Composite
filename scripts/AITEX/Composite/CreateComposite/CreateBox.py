import gmsh
import glob
import os
import numpy as np
from CompositeSandwich.box_labeling import box_labeling
from .SetNames import SetNames
from ..inp.are_coplanar import are_coplanar



def CreateBox(params_yarns,output_folder):


    Lx = params_yarns["Lx"]
    Ly = params_yarns["Ly"]
    h = params_yarns["h"]
    z0 = 2*(params_yarns["z0"] - 0.5*h)
    zL = h*(len(params_yarns["trajs_layers"]))*2 
    zT = z0 + zL
    radius = params_yarns["r"]

    # load all the geometries
    files_yarns = glob.glob(os.path.join(*output_folder,"*.brep"))

    # ==================================================
    # Set names and sort
    names,files_yarns = SetNames(files_yarns)
    # ==================================================

    gmsh.initialize()
    gmsh.clear()



    fc_mesh_min = params_yarns["fc_mesh_min"]
    fc_mesh_max = params_yarns["fc_mesh_max"]
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", radius*fc_mesh_min)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", radius*fc_mesh_max)

    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 30)
    gmsh.option.setNumber("Mesh.Algorithm", 2)
    gmsh.option.setNumber("Mesh.Optimize", 1)
    gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)
    gmsh.option.setNumber("Mesh.HighOrderOptimize", 2)
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
    big_box = gmsh.model.occ.addBox(0, 0, -zT/2, 
                        Lx, Ly,zT)

    mid_box = gmsh.model.occ.addBox(0 , 0 , -z0/2, 
                        Lx, Ly, z0)


    # cut the box 
    gmsh.model.occ.cut([(3, big_box)], [(3, mid_box)], removeTool=False)

    gmsh.model.occ.synchronize()


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

    names_box = ["box_minus","alma","box_plus"]

    for name, ibox in zip(names_box,final_obj_box):
        gmsh.model.addPhysicalGroup(3, [ibox[1]], tag=-1,name=name)


    box_labeling(final_obj_box[0][1],"minus")
    box_labeling(final_obj_box[1][1],"alma")
    box_labeling(final_obj_box[2][1],"plus")

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


    box2maxlen = lambda box: np.max([
        box[3] - box[0], 
        box[4] - box[1], 
        box[5] - box[2]
    ])
    gBB_surf = [box2maxlen(gmsh.model.occ.getBoundingBox(2, isurf[1]) )
                for isurf in all_surfaces]

    x0_surfaces = surfaces_limits[0]
    xL_surfaces = surfaces_limits[2]

    COM_x0 = [COM[i] for i in x0_surfaces]
    COM_xL = [COM[i] for i in xL_surfaces]

    gBB_s_x0 = [gBB_surf[i] for i in x0_surfaces]
    gBB_s_xL = [gBB_surf[i] for i in xL_surfaces]

    # sort by y and z
    id_com = sorted(range(len(COM_x0)), 
                    key=lambda k: (COM_x0[k][2],
                                COM_x0[k][1],
                                gBB_s_x0[k]))

    x0_surfaces = [x0_surfaces[i] for i in id_com]
    COM_x0      = [COM_x0[i] for i in id_com]


    id_com = sorted(range(len(COM_xL)), 
                    key=lambda k: (COM_xL[k][2],
                                COM_xL[k][1],
                                gBB_s_xL[k]))

    xL_surfaces = [xL_surfaces[i] for i in id_com]
    COM_xL      = [COM_xL[i] for i in id_com]


    t = [ 1, 0, 0, -Lx ,\
        0, 1, 0, 0   ,\
        0, 0, 1, 0   ,\
        0, 0, 0, 0    ]

    # for ix0, ixL in zip(x0_surfaces, xL_surfaces):
    #     gmsh.model.mesh.setPeriodic(2, [all_surfaces[ix0][1]], [all_surfaces[ixL][1]], t)

    # physical group index x0_1 x0_2 x0_3 ...

    for i, isurf in enumerate(x0_surfaces):
        gmsh.model.addPhysicalGroup(2, [all_surfaces[isurf][1]], tag=-1, name="x0_%s" % (i+1))

    for i, isurf in enumerate(xL_surfaces):
        gmsh.model.addPhysicalGroup(2, [all_surfaces[isurf][1]], tag=-1, name="xL_%s" % (i+1))



    gmsh.model.occ.synchronize()

    # save geo ad brep
    gmsh.write(os.path.join(*output_folder,"composite.brep"))


    # Sincronizar geometría
    gmsh.model.geo.synchronize()

    # Obtener todas las superficies
    all_surfaces = gmsh.model.getEntities(2)

    # Obtener las superficies con Physical Groups
    physical_surfaces = set()
    for dim, tag in gmsh.model.getPhysicalGroups():
        physical_surfaces.update(gmsh.model.getEntitiesForPhysicalGroup(dim, tag))

    # Identificar superficies sin Physical Groups
    surfaces_without_physical = [s for s in all_surfaces if s not in physical_surfaces]

    # Eliminar superficies sin Physical Groups
    for dim, tag in surfaces_without_physical:
        gmsh.model.geo.remove([(dim, tag)])

    # Sincronizar después de eliminar
    gmsh.model.geo.synchronize()

    print(50*"*")
    print("The Geometry is ready to be meshed")
    print("Meshing the geometry ...")
    #

    # gmsh.option.setNumber("Mesh.OptimizeThreshold", 0.1)

    try:
        gmsh.model.mesh.generate(3)
    except Exception as e:
        print("Error: ",e)
        gmsh.fltk.run()

    gmsh.model.mesh.setOrder(2)
    # inp 
    gmsh.write(os.path.join(*output_folder,"composite.inp"))

    gmsh.finalize()


    return params_yarns