import gmsh
import numpy as np
def CreateCompositeMinRVE(params):

    trajs  = params["trajs"]
    radius = params["radius"]
    r      = params["r"]
    files  = params["files"]
    output = params["output"]


    gmsh.initialize()
    #verbose 0
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add("composite")

    for i in range(len(trajs)):
        gmsh.merge(files[i])

    yarns = gmsh.model.getEntities(3)
    dz = 3*radius
    box = gmsh.model.occ.addBox(0  , 0  , -dz/2, 
                                2*r, 2*r, dz)
    # cut 
    gmsh.model.occ.synchronize()

    gmsh.model.occ.cut([(3, box)], yarns, removeTool=False)
    # 
    gmsh.model.occ.synchronize()

    # Obtener las caras de la caja cortada
    box_faces = gmsh.model.getBoundary([(3, box)], oriented=False, recursive=False)
    box_faces = [face[1] for face in box_faces]

    # create all 3d volume

    gmsh.model.occ.synchronize()

    all_volumes = gmsh.model.getEntities(3)
    # get mass center of each volume
    volumes = []
    for volume in all_volumes:
        volumes.append( (volume, gmsh.model.occ.getCenterOfMass(3, volume[1])) )
    # sort by x
    volumes = sorted(volumes, key=lambda x: x[1][0])
    # 
    names =[ "yarn_1","box", "yarn_2"] 

    for i,volume in enumerate(volumes):
        gmsh.model.addPhysicalGroup(3, [volume[0][1]], i+1)
        gmsh.model.setPhysicalName(3, i+1, names[i])

    surfaces = []
    all_surfaces = gmsh.model.getEntities(2)

    for surface in all_surfaces:
        surfaces.append( (surface, gmsh.model.occ.getCenterOfMass(2, surface[1])) )

    def labeling(ph_surfaces,label):
    
        ph_tags = [ ph[0][1] for ph in ph_surfaces ]
        lens = [ len(gmsh.model.getBoundary([ph[0]], oriented=False, recursive=False)) 
                for ph in ph_surfaces ]
        
        ph_label = gmsh.model.addPhysicalGroup(2, ph_tags, -1)
        gmsh.model.setPhysicalName(2, ph_label, "face_"+label)

        # lens = 1 is circular face and lens = 5 is rectangular face with circular hole

        idx_circular    = lens.index(1)
        idx_rectangular = lens.index(5)

        ph_label_circular = gmsh.model.addPhysicalGroup(2, [ph_surfaces[idx_circular][0][1]], -1)
        gmsh.model.setPhysicalName(2, ph_label_circular, "face_circular_"+label)

        ph_label_rectangular = gmsh.model.addPhysicalGroup(2, [ph_surfaces[idx_rectangular][0][1]], -1)
        gmsh.model.setPhysicalName(2, ph_label_rectangular, "face_rectangular"+label)  

        tags = {
            "circle" : ph_surfaces[idx_circular][0][1],
            "rectangular" : ph_surfaces[idx_rectangular][0][1],
            "ph_label_circular" : ph_label_circular,
            "ph_label_rectangular" : ph_label_rectangular
        } 

        return tags

   # ================================================================================================= 

    surfaces = sorted(surfaces, key=lambda x: x[1][0])
    ##
    ph_surfaces =[ surfaces[0], 
                   surfaces[1] ]
    
    tags_min_x = labeling(ph_surfaces,"xmin")


    ph_surfaces =[ surfaces[-1],
                   surfaces[-2] ]
    
    tags_max_x = labeling(ph_surfaces,"xmax")
    
    
   # ================================================================================================= 
    surfaces = sorted(surfaces, key=lambda x: x[1][1])
    ##
    ph_surfaces =[   surfaces[0],
                     surfaces[1] ]

    tags_min_y = labeling(ph_surfaces,"ymin")

    ph_surfaces =[   surfaces[-1],
                     surfaces[-2] ]
    
    tags_max_y = labeling(ph_surfaces,"ymax")

    # =================================================================================================

    tx = -2*r
    ty = 0
    tz = 0

    transformation = [  1 ,0 ,0 ,tx ,
                        0 ,1 ,0 ,ty ,
                        0 ,0 ,1 ,tz ,
                        0 ,0 ,0 ,1]
    

    gmsh.model.mesh.setPeriodic(2,[tags_min_x["circle"]] ,
                                  [tags_max_x["circle"]] ,transformation)
    

    gmsh.model.mesh.setPeriodic(2,[tags_min_x["rectangular"]] ,
                                  [tags_max_x["rectangular"]] ,transformation)
    tx = 0
    ty = -2*r
    tz = 0

    transformation = [  1 ,0 ,0 ,tx ,
                        0 ,1 ,0 ,ty ,
                        0 ,0 ,1 ,tz ,
                        0 ,0 ,0 ,1]

    gmsh.model.mesh.setPeriodic(2,[tags_min_y["circle"]] ,
                                  [tags_max_y["circle"]] ,transformation)
    
    gmsh.model.mesh.setPeriodic(2,[tags_min_y["rectangular"]] ,
                                  [tags_max_y["rectangular"]] ,transformation)



    surfaces = sorted(surfaces, key=lambda x: x[1][2])

    ph_label = gmsh.model.addPhysicalGroup(2, [surfaces[0][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph_label, "face_zmin")

    ph_label = gmsh.model.addPhysicalGroup(2, [surfaces[-1][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph_label, "face_zmax")


    gmsh.model.occ.synchronize()

    # =======================================================================
    # face_circular_xmin and face_circular_xmax are the same must periodic
    # =======================================================================
    # 
        

    # mesh
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", radius*0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 4*radius)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 20)
    gmsh.option.setNumber("Mesh.AngleSmoothNormals", 10)
    gmsh.option.setNumber("Mesh.Smoothing", 10)	
    gmsh.option.setNumber("Mesh.Algorithm", 2)

    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.setOrder(2)

    getnodes = lambda tag: np.unique(gmsh.model.mesh.getNodesByElementType(2, tag)[0] )

    
    results ={
        "circle_x_min"      : getnodes(tags_min_x["circle"]),
        "circle_x_max"      : getnodes(tags_max_x["circle"]),
        "circle_y_min"      : getnodes(tags_min_y["circle"]),
        "circle_y_max"      : getnodes(tags_max_y["circle"]),
        "rectangular_x_min" : getnodes(tags_min_x["rectangular"]),
        "rectangular_x_max" : getnodes(tags_max_x["rectangular"]),
        "rectangular_y_min" : getnodes(tags_min_y["rectangular"]),
        "rectangular_y_max" : getnodes(tags_max_y["rectangular"])
    } 

    results["x_min"] = np.concatenate([results["circle_x_min"],results["rectangular_x_min"]])
    results["x_max"] = np.concatenate([results["circle_x_max"],results["rectangular_x_max"]])

    results["y_min"] = np.concatenate([results["circle_y_min"],results["rectangular_y_min"]])
    results["y_max"] = np.concatenate([results["circle_y_max"],results["rectangular_y_max"]]) 

    # unique nodes
    results["x_min"] = np.unique(results["x_min"])
    results["x_max"] = np.unique(results["x_max"])
    results["y_min"] = np.unique(results["y_min"])
    results["y_max"] = np.unique(results["y_max"])

    # save in inp format
    gmsh.write(output)


    gmsh.finalize()

    return results