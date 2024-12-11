import gmsh
import numpy as np
from CompositeSandwich.CreateLayerYarns import CreateLayerYarns
from .CreatePlainLayer import CreatePlainLayer

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

    # named boundaries
    #
    box_mid_faces = gmsh.model.getBoundary([(3,box_mid)], oriented=False)

    surfaces = []

    for surface in box_mid_faces:
        surfaces.append((surface,
                         gmsh.model.occ.getCenterOfMass(2,surface[1])))

    surfaces = sorted(surfaces, key=lambda x: x[1][0])

    box_mid_xmin = surfaces[0][0][1]
    box_mid_xmax = surfaces[-1][0][1]

    ph = gmsh.model.addPhysicalGroup(2,[box_mid_xmin], -1)
    gmsh.model.setPhysicalName(2, ph, "box_mid_xmin")

    ph = gmsh.model.addPhysicalGroup(2,[box_mid_xmax], -1)
    gmsh.model.setPhysicalName(2, ph, "box_mid_xmax")

    surfaces = sorted(surfaces, key=lambda x: x[1][1])

    box_mid_ymin = surfaces[0][0][1]
    box_mid_ymax = surfaces[-1][0][1]

    ph = gmsh.model.addPhysicalGroup(2,[box_mid_ymin], -1)
    gmsh.model.setPhysicalName(2, ph, "box_mid_ymin")

    ph = gmsh.model.addPhysicalGroup(2,[box_mid_ymax], -1)
    gmsh.model.setPhysicalName(2, ph, "box_mid_ymax")


    # create yarns
    
    gmsh.model.occ.synchronize()

    z_span = [0,Lz+h_mid]
    angle_span = [0,0.5*np.pi]


    layers = []
    NLayers = params["NLayers"]

    for i in range(NLayers):
        layer_params ={
            "layer_name" : "ly_"+str(i+1),
            "z" : z_span[i],
            "Lz" : Lz,
            "angle" : angle_span[i]
        } 
        tags_min_x, tags_max_x, tags_min_y, tags_max_y = CreateLayerYarns(params,layer_params)
        layers.append({ 
            "layer_name" : layer_params["layer_name"],
            "tags_min_x" : tags_min_x,
            "tags_max_x" : tags_max_x,
            "tags_min_y" : tags_min_y,
            "tags_max_y" : tags_max_y
        })


    if NLayers == 1:
        CreatePlainLayer(trajs, xlims, ylims, Lx, Ly, Lz, h_mid, radius)
    # =======================================================================
    # face_circular_xmin and face_circular_xmax are the same must periodic
    # =======================================================================
    # 

    # mesh
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", radius*0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", radius)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 20)
    gmsh.option.setNumber("Mesh.AngleSmoothNormals", 10)
    gmsh.option.setNumber("Mesh.Smoothing", 10)	
    gmsh.option.setNumber("Mesh.Algorithm", 2)

    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.setOrder(2)

    getnodes = lambda tag: np.unique(gmsh.model.mesh.getNodesByElementType(2, tag)[0] )


    tag_min_x_circles = np.concatenate([ layer["tags_min_x"]["circles"] for layer in layers ])
    tags_min_x_rect   = np.array([ layer["tags_min_x"]["rectangle"] 
                                  for layer in layers ])
    tags_min_x = np.concatenate([tag_min_x_circles,tags_min_x_rect,[box_mid_xmin]])

    tag_max_x_circles = np.concatenate([ layer["tags_max_x"]["circles"] for layer in layers ])
    tags_max_x_rect   = np.array([ layer["tags_max_x"]["rectangle"] for layer in layers ])
    tags_max_x = np.concatenate([tag_max_x_circles,tags_max_x_rect,[box_mid_xmax]])

    tag_min_y_circles = np.concatenate([ layer["tags_min_y"]["circles"] for layer in layers ])
    tags_min_y_rect   = np.array([ layer["tags_min_y"]["rectangle"] for layer in layers ])
    tags_min_y = np.concatenate([tag_min_y_circles,tags_min_y_rect,[box_mid_ymin]])

    tag_max_y_circles = np.concatenate([ layer["tags_max_y"]["circles"] for layer in layers ])
    tags_max_y_rect   = np.array([ layer["tags_max_y"]["rectangle"] for layer in layers ])
    tags_max_y = np.concatenate([tag_max_y_circles,tags_max_y_rect,[box_mid_ymax]])

    
    # unique 
    tags_min_x = np.unique(tags_min_x)
    tags_max_x = np.unique(tags_max_x)
    tags_min_y = np.unique(tags_min_y)
    tags_max_y = np.unique(tags_max_y)

    nodes_min_x = np.concatenate([ getnodes(i) for i in tags_min_x ])
    nodes_max_x = np.concatenate([ getnodes(i) for i in tags_max_x ])
    nodes_min_y = np.concatenate([ getnodes(i) for i in tags_min_y ])
    nodes_max_y = np.concatenate([ getnodes(i) for i in tags_max_y ])


    results = {
        "x_min" : np.unique(nodes_min_x),
        "x_max" : np.unique(nodes_max_x),
        "y_min" : np.unique(nodes_min_y),
        "y_max" : np.unique(nodes_max_y)
    }

    try:
        gmsh.fltk.run()
    except:
        pass
    # save in inp format
    gmsh.write(output)

    gmsh.finalize()


    params["results"] = results
    return params