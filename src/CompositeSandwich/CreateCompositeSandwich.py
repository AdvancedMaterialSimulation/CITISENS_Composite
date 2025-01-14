import gmsh
import numpy as np
from CompositeSandwich.CreateLayerYarns import CreateLayerYarns
from .CreatePlainLayer import CreatePlainLayer
from .box_labeling import box_labeling
def CreateCompositeSandwich(params):

    radius = params["radius"]
    output = params["inp_file"]

    gmsh.initialize()
    #verbose 0
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.Verbosity", 0)

    gmsh.model.add("composite")

    h_mid = 0.5*radius
    Lz = 3*radius
    r      = params["r"]
    trajs_layers = params["trajs_layers"]
    trajs = trajs_layers[0]
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

    surfaces = sorted(surfaces, key=lambda x: x[1][2])

    box_mid_zmin = surfaces[0][0][1]
    box_mid_zmax = surfaces[-1][0][1]

    ph = gmsh.model.addPhysicalGroup(2,[surfaces[0][0][1]], -1)
    gmsh.model.setPhysicalName(2, ph, "box_mid_zmin")

    ph = gmsh.model.addPhysicalGroup(2,[surfaces[-1][0][1]], -1)    
    gmsh.model.setPhysicalName(2, ph, "box_mid_zmax")

    # create yarns
    
    gmsh.model.occ.synchronize()

    z_span = [0,Lz+h_mid]


    layers = []
    NLayers = params["NLayers"]

    for i in range(NLayers):

        files_layer = [ file for file in params["files"] 
                             if "layer_"+str(i+1) in file ]
        
        layer_params =  {
                        "layer_name"    : "ly_"+str(i+1),
                        "z"             : z_span[i],
                        "Lz"            : Lz,
                        "files_layer"   : files_layer,
                        "trajs"         : trajs_layers[i]
                        } 

        tags_min_x, tags_max_x, tags_min_y, tags_max_y,tags_min_z,tags_max_z,holow_box = CreateLayerYarns(params,layer_params)
        layers.append({ 
            "layer_name" : layer_params["layer_name"],
            "tags_min_x" : tags_min_x,
            "tags_max_x" : tags_max_x,
            "tags_min_y" : tags_min_y,
            "tags_max_y" : tags_max_y,
            "tags_min_z" : tags_min_z,
            "tags_max_z" : tags_max_z,
            "holow_box"  : holow_box
        })


    # remove duplicate  
    
    gmsh.model.occ.synchronize()

    
    if NLayers == 1:
       holow_box_plain,cc,tag_split_plain =  CreatePlainLayer(trajs, xlims, ylims, Lx, Ly, Lz, h_mid, radius) 
       tag_split_plain_x = [it for it in tag_split_plain if it["plane"] == "x"]
       x0_tag_plain = tag_split_plain_x[0]["results"]["ph_rect"]
       xL_tag_plain = tag_split_plain_x[1]["results"]["ph_rect"]

       tag_split_plain_y = [it for it in tag_split_plain if it["plane"] == "y"]

       # tag elements from physical group
    gmsh.model.occ.synchronize()

    # compount box mid with layers
    holow_box = [ layer["holow_box"][0][0][1] for layer in layers ]

    if NLayers == 1:
        holow_box = holow_box + [holow_box_plain[0][0][1]]
        
    volumen_fuse = [ (3,box_mid) ] + [ (3,box) for box in holow_box ]
    fuse_results = gmsh.model.occ.fragment(volumen_fuse[0:], volumen_fuse[1:])
    gmsh.model.occ.synchronize()

    volumen_fuse_list = [ ]

    for i in range(len(fuse_results[0])):
        volumen_fuse_list.append({
            "volumen" : fuse_results[0][i][0],
            "tags" : fuse_results[0][i][1],
            "pos" : gmsh.model.occ.getCenterOfMass(3,fuse_results[0][i][1])
        })

    # sort by z
    volumen_fuse_list = sorted(volumen_fuse_list, key=lambda x: x["pos"][2])

    # add physical group
    ph = gmsh.model.addPhysicalGroup(3,[volumen_fuse_list[0]["tags"]], -1)
    gmsh.model.setPhysicalName(3, ph, "box_1")

    ph = gmsh.model.addPhysicalGroup(3,[volumen_fuse_list[1]["tags"]], -1)
    gmsh.model.setPhysicalName(3, ph, "box_mid_y")

    ph = gmsh.model.addPhysicalGroup(3,[volumen_fuse_list[2]["tags"]], -1)
    gmsh.model.setPhysicalName(3, ph, "box_2")

    ph_list_ly_1   = box_labeling(volumen_fuse_list[0]["tags"],"layer_1")
    ph_list_ly_mid = box_labeling(volumen_fuse_list[1]["tags"],"layer_mid")
    ph_list_ly_2   = box_labeling(volumen_fuse_list[2]["tags"],"layer_2")

    tags_min_x_rect =  ph_list_ly_1["x0"] + ph_list_ly_mid["x0"] + ph_list_ly_2["x0"] 
    tags_max_x_rect =  ph_list_ly_1["xL"] + ph_list_ly_mid["xL"] + ph_list_ly_2["xL"] 

    if NLayers == 1:
        x0_list = gmsh.model.getEntitiesForPhysicalGroup(2,x0_tag_plain).tolist()
        xL_list = gmsh.model.getEntitiesForPhysicalGroup(2,xL_tag_plain).tolist()
        tags_min_x_rect = tags_min_x_rect + x0_list
        tags_max_x_rect = tags_max_x_rect + xL_list

    tags_min_y_rect =  ph_list_ly_1["y0"] + ph_list_ly_mid["y0"] + ph_list_ly_2["y0"] 
    tags_max_y_rect =  ph_list_ly_1["yL"] + ph_list_ly_mid["yL"] + ph_list_ly_2["yL"] 


    gmsh.model.occ.synchronize()


    # =======================================================================
    # face_circular_xmin and face_circular_xmax are the same must periodic
    # =======================================================================
    # 

    # mesh
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", radius*0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", radius)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 25)
    gmsh.option.setNumber("Mesh.AngleSmoothNormals", 10)
    gmsh.option.setNumber("Mesh.Smoothing", 10)	
    gmsh.option.setNumber("Mesh.Algorithm", 2)

    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.setOrder(2)

    gmsh.model.occ.synchronize()
    gmsh.write(output)
    getnodes = lambda tag: np.unique(gmsh.model.mesh.getNodesByElementType(2, tag)[0] )


    tag_min_x_circles = np.concatenate([ layer["tags_min_x"]["circles"] for layer in layers ])

    tags_min_x = np.concatenate([tag_min_x_circles,tags_min_x_rect])

    tag_max_x_circles = np.concatenate([ layer["tags_max_x"]["circles"] for layer in layers ])
    tags_max_x = np.concatenate([tag_max_x_circles,tags_max_x_rect])

    tag_min_y_circles = np.concatenate([ layer["tags_min_y"]["circles"] for layer in layers ])
    tags_min_y = np.concatenate([tag_min_y_circles,tags_min_y_rect])

    tag_max_y_circles = np.concatenate([ layer["tags_max_y"]["circles"] for layer in layers ])
    tags_max_y = np.concatenate([tag_max_y_circles,tags_max_y_rect])

    if NLayers == 1:

        rxr = np.array(tag_split_plain_y[0]["results"]["circles"])
        tags_min_y = np.concatenate([tags_min_y,rxr])

        rxr = np.array(tag_split_plain_y[1]["results"]["circles"])
        tags_max_y = np.concatenate([tags_max_y,rxr])


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

    # try:
    #     gmsh.fltk.run()
    # except:
    #     pass
    # save in inp format
    gmsh.write(output)
    # 
    # replace .inp -> comsol .msh
    gmsh.write(output.replace(".inp",".msh"))

    gmsh.finalize()


    params["results"] = results
    return params