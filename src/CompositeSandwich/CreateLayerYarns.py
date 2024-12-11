import gmsh
import numpy as np
def labeling(ph_surfaces,label):
    

    ph_tags = [ ph[0][1] for ph in ph_surfaces ]
    lens = [ len(gmsh.model.getBoundary([ph[0]], oriented=False, recursive=False)) 
            for ph in ph_surfaces ]
    
    ph_label = gmsh.model.addPhysicalGroup(2, ph_tags, -1)
    gmsh.model.setPhysicalName(2, ph_label, "face_"+label)

    # lens = 1 is circular face and lens = 5 is rectangular face with circular hole
    try:
        idx_circular    = lens.index(1)
    except:
        print("Error: The circular face is not found")
        gmsh.fltk.run()
   # the other  is rectangular face with circular hole
    idx_rectangular =[i for i in range(len(lens)) if i != idx_circular][0] 

    ph_label_circular = gmsh.model.addPhysicalGroup(2, [ph_surfaces[idx_circular][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph_label_circular, "face_circular_"+label)

    ph_label_rectangular = gmsh.model.addPhysicalGroup(2, [ph_surfaces[idx_rectangular][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph_label_rectangular, "face_rectangular_"+label)  

    tags = {
        "circle" : ph_surfaces[idx_circular][0][1],
        "rectangular" : ph_surfaces[idx_rectangular][0][1],
        "ph_label_circular" : ph_label_circular,
        "ph_label_rectangular" : ph_label_rectangular
    } 

    return tags

def CreateLayerYarns(params,params_layer):

    trajs  = params["trajs"]
    r      = params["r"]
    files  = params["files"]
    xlims  = params["xlims"]
    ylims  = params["ylims"]
    Lx     = xlims[1] - xlims[0]
    Ly     = ylims[1] - ylims[0]


    Lz     = params_layer["Lz"]
    z      = params_layer["z"] + Lz/2

    layer_name = params_layer["layer_name"]
    angle = params_layer["angle"]
    #sync
    gmsh.model.occ.synchronize()  
    pre_exist_volumes = gmsh.model.getEntities(3)
    pre_exist_surfaces = gmsh.model.getEntities(2)

    for i in range(len(trajs)):
        gmsh.merge(files[i])

    # get yarns

    yarns = gmsh.model.getEntities(3)
    yarns = [i for i in yarns if i not in pre_exist_volumes]

    # translate yarns
    gmsh.model.occ.translate(yarns, 0, 0, z) 
   # rotate yarns
   # 
    xrot = xlims[0] + Lx/2 
    yrot = ylims[0] + Ly/2
    zrot = 0
    gmsh.model.occ.rotate(yarns, 
                          xrot, yrot, zrot, 
                          0, 0, 1, angle) 

    dz = Lz

    box = gmsh.model.occ.addBox(xlims[0], ylims[0]   , z-dz/2, 
                                Lx      , Ly         , dz)
    
    # cut 
    gmsh.model.occ.synchronize()

    hollow_box =  gmsh.model.occ.cut([(3, box)], yarns, removeTool=False)
    # 
    gmsh.model.occ.synchronize()

    # Obtener las caras de la caja cortada
    box_faces = gmsh.model.getBoundary([(3, box)], oriented=False, recursive=False)
    box_faces = [face[1] for face in box_faces]

    # create all 3d volume

    gmsh.model.occ.synchronize()

    all_volumes = gmsh.model.getEntities(3)
    all_volumes = [i for i in all_volumes if i not in pre_exist_volumes]

    # get mass center of each volume
    volumes = []
    for volume in all_volumes:
        volumes.append( (volume, gmsh.model.occ.getCenterOfMass(3, volume[1])) )
    # sort by x

   # 
   # 
    xmid = xlims[0] + Lx/2
    ymid = ylims[0] + Ly/2
    zmid = z + dz/2 
    rmid = np.array([xmid,ymid,zmid])

    volumes = sorted(volumes, key=lambda x: np.linalg.norm(np.array(x[1])-rmid))

    volumen_box = volumes[0]
    volumes = volumes[1:]

    volumes = sorted(volumes, key=lambda x: x[1][0])
    volumes = [volumen_box] + volumes
    # 
    names =[layer_name +"_box"] + [layer_name+"_yarn_"+str(i) 
                       for i in range(1,len(volumes)) ]  
    
    for i,volume in enumerate(volumes):
        ph = gmsh.model.addPhysicalGroup(3, [volume[0][1]], -1)
        gmsh.model.setPhysicalName(3, ph, names[i])

    surfaces = []
    all_surfaces = gmsh.model.getEntities(2)
    all_surfaces = [i for i in all_surfaces if i not in pre_exist_surfaces]

    for surface in all_surfaces:
        surfaces.append( (surface, gmsh.model.occ.getCenterOfMass(2, surface[1])) )


   # ================================================================================================= 

    surfaces = sorted(surfaces, key=lambda x: x[1][0])
   # compute number of aristas
    lens = [ len(gmsh.model.getBoundary([surface[0]], oriented=False, recursive=False)) 
            for surface in surfaces ] 
    ##
    ph_surfaces =[ surfaces[0], 
                   surfaces[1] ]
    
    tags_min_x = labeling(ph_surfaces,layer_name+"_xmin")


    ph_surfaces =[ surfaces[-1],
                   surfaces[-2] ]
    
    tags_max_x = labeling(ph_surfaces,layer_name+"_xmax")
    
    
   # ================================================================================================= 
    surfaces = sorted(surfaces, key=lambda x: x[1][1])
    ##
    ph_surfaces =[   surfaces[0],
                     surfaces[1] ]

    tags_min_y = labeling(ph_surfaces,layer_name+"_ymin")

    ph_surfaces =[   surfaces[-1],
                     surfaces[-2] ]
    
    tags_max_y = labeling(ph_surfaces,layer_name+"_ymax")

    # =================================================================================================

    # tx = -2*r
    # ty = 0
    # tz = 0

    # transformation = [  1 ,0 ,0 ,tx ,
    #                     0 ,1 ,0 ,ty ,
    #                     0 ,0 ,1 ,tz ,
    #                     0 ,0 ,0 ,1]
    

    # gmsh.model.mesh.setPeriodic(2,[tags_min_x["circle"]] ,
    #                               [tags_max_x["circle"]] ,transformation)
    

    # gmsh.model.mesh.setPeriodic(2,[tags_min_x["rectangular"]] ,
    #                               [tags_max_x["rectangular"]] ,transformation)
    # tx = 0
    # ty = -2*r
    # tz = 0

    # transformation = [  1 ,0 ,0 ,tx ,
    #                     0 ,1 ,0 ,ty ,
    #                     0 ,0 ,1 ,tz ,
    #                     0 ,0 ,0 ,1]

    # gmsh.model.mesh.setPeriodic(2,[tags_min_y["circle"]] ,
    #                               [tags_max_y["circle"]] ,transformation)
    
    # gmsh.model.mesh.setPeriodic(2,[tags_min_y["rectangular"]] ,
    #                               [tags_max_y["rectangular"]] ,transformation)


    surfaces = sorted(surfaces, key=lambda x: x[1][2])

    ph_label = gmsh.model.addPhysicalGroup(2, [surfaces[0][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph_label, "face_zmin_" + layer_name)

    ph_label = gmsh.model.addPhysicalGroup(2, [surfaces[-1][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph_label, "face_zmax_" + layer_name)


    gmsh.model.occ.synchronize()

    return tags_min_x, tags_max_x, tags_min_y, tags_max_y
