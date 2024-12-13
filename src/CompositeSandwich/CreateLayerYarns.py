import gmsh
import numpy as np
from .process_surfaces_in_plane import process_surfaces_in_plane

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

    r      = params["r"]
    xlims  = params["xlims"]
    ylims  = params["ylims"]
    Lx     = xlims[1] - xlims[0]
    Ly     = ylims[1] - ylims[0]

    trajs  = params_layer["trajs"]
    files  = params_layer["files_layer"]
    Lz     = params_layer["Lz"]
    z      = params_layer["z"] + Lz/2

    layer_name = params_layer["layer_name"]
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


    # Uso de la función para los cuatro casos

    cases = [(0, 0,  'x',"0"), 
             (0, Lx, 'x',"L"), 
             (1, 0,  'y',"0"),
             (1, Ly, 'y',"L")]
    
    tags_split = []
    for coord, value, plane,name in cases:
        results = process_surfaces_in_plane(surfaces, coord, value, 
                                            layer_name, plane,name)
        
        tags_split.append({
            "cord" : coord,
            "value" : value,
            "plane" : plane,
            "name" : name,
            "results" : results
        })

   # ================================================================================================= 

    zpos = [surface[1][2] for surface in surfaces]
    surfaces_in_z0 = [surface for i,surface in enumerate(surfaces) if np.abs(zpos[i] - (z-dz/2)) < 1e-6]
    surfaces_in_zLz = [surface for i,surface in enumerate(surfaces) if np.abs(zpos[i] - (z + dz/2 )) < 1e-6]

    if len(surfaces_in_z0) !=1:
        raise ValueError("Error: The number of surfaces in z = 0 is not 1")
    if len(surfaces_in_zLz) !=1:
        raise ValueError("Error: The number of surfaces in z = Lz is not 1")
    
    surfaces_in_z0 = surfaces_in_z0[0]
    surfaces_in_zLz = surfaces_in_zLz[0]

    ph = gmsh.model.addPhysicalGroup(2, [surfaces_in_z0[0][1]], -1)
    gmsh.model.setPhysicalName(2, ph, layer_name + "_z0")

    ph = gmsh.model.addPhysicalGroup(2, [surfaces_in_zLz[0][1]], -1)
    gmsh.model.setPhysicalName(2, ph, layer_name + "_zLz")

  
   # compute number of aristas

    # =================================================================================================
    gmshtol = 1e-5
    gmsh.option.setNumber("Geometry.Tolerance", gmshtol)

    gmsh.model
    # =================================================================================================
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

    gmsh.model.mesh.setPeriodic(2,tags_min_x["rectangle"] ,
                                  tags_max_x["rectangle"] ,transformation)
    
    gmsh.model.mesh.setPeriodic(2,tags_min_x["circles"] ,
                                  tags_max_x["circles"] ,transformation)
    

    tx = 0
    ty = -Ly

    transformation = [  1 ,0 ,0 ,tx ,
                        0 ,1 ,0 ,ty ,
                        0 ,0 ,1 ,tz ,
                        0 ,0 ,0 ,0]


    tags_max_y = [ i for i in tags_split if i["plane"] == "y"
                                            and i["value"] == Ly][0]["results"]
    tags_min_y = [ i for i in tags_split if i["plane"] == "y"
                                            and i["value"] == 0 ][0]["results"]
    
    gmsh.model.mesh.setPeriodic(2,tags_min_y["rectangle"] ,
                                  tags_max_y["rectangle"] ,transformation)
    
    gmsh.model.mesh.setPeriodic(2,tags_min_y["circles"] ,
                                    tags_max_y["circles"] ,transformation)
    


    # find  the surface where z=0 and z=Lz
    tags_max_z = surfaces_in_zLz[0][1]
    tags_min_z = surfaces_in_z0[0][1]
    gmsh.model.occ.synchronize()

    return tags_min_x, tags_max_x, tags_min_y, tags_max_y, tags_min_z, tags_max_z,hollow_box
