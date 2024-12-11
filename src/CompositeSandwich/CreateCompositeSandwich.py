import gmsh
import numpy as np
from CompositeSandwich.CreateLayerYarns import CreateLayerYarns


def CreateCompositeSandwich(params):

    radius = params["radius"]
    output = params["inp_file"]

    gmsh.initialize()
    #verbose 0
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.model.add("composite")

    h_mid = 0.5*radius
    Lz = 3*radius
    r      = params["r"]
    trajs = params["trajs"]
    all_points = np.concatenate(trajs)
    xlims = [np.min(all_points[:,0]),np.max(all_points[:,0])]
    ylims = [np.min(all_points[:,1]),np.max(all_points[:,1])]
    params["xlims"] = xlims
    params["ylims"] = ylims
    Lx = xlims[1] - xlims[0]
    Ly = ylims[1] - ylims[0]

    box_mid = gmsh.model.occ.addBox(xlims[0] , ylims[0] , Lz, 
                                    Lx       , Ly       , h_mid)
    
    gmsh.model.occ.synchronize()

   # add physical group
   # 
    ph = gmsh.model.addPhysicalGroup(3,[box_mid], -1)
    gmsh.model.setPhysicalName(3, ph, "box_mid")  
    
    gmsh.model.occ.synchronize()

    z_span = [0,Lz+h_mid]
    angle_span = [0,0.5*np.pi]



    for i in range(2):
        layer_params ={
            "layer_name" : "layer_"+str(i+1),
            "z" : z_span[i],
            "Lz" : Lz,
            "angle" : angle_span[i]
        } 
        tags_min_x, tags_max_x, tags_min_y, tags_max_y = CreateLayerYarns(params,layer_params)


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


    try:
        gmsh.fltk.run()
    except:
        pass
    # save in inp format
    gmsh.write(output)
    gmsh.write("output.msh")


    gmsh.finalize()


    params["results"] = results
    return params