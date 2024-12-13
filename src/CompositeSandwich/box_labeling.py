
import gmsh
import numpy as np

def box_labeling(tag, label):

    
    volumen = gmsh.model.getBoundary([(3,tag)], oriented=False)

    surfaces = []
    for surface in volumen:
        surfaces.append({
            "surface" : surface[1],
            "pos" : gmsh.model.occ.getCenterOfMass(2,surface[1])
        })

    positions = [i["pos"] for i in surfaces]
    positions = np.array(positions)

    xlims = [np.min(positions[:,0]), np.max(positions[:,0])]
    ylims = [np.min(positions[:,1]), np.max(positions[:,1])]
    zlims = [np.min(positions[:,2]), np.max(positions[:,2])]

    surfaces_x0 = [ i for i in surfaces if np.abs(i["pos"][0] - xlims[0]) < 1e-6 ]
    surfaces_xL = [ i for i in surfaces if np.abs(i["pos"][0] - xlims[1]) < 1e-6 ]

    surfaces_y0 = [ i for i in surfaces if np.abs(i["pos"][1] - ylims[0]) < 1e-6 ]
    surfaces_yL = [ i for i in surfaces if np.abs(i["pos"][1] - ylims[1]) < 1e-6 ]

    surfaces_z0 = [ i for i in surfaces if np.abs(i["pos"][2] - zlims[0]) < 1e-6 ]
    surfaces_zL = [ i for i in surfaces if np.abs(i["pos"][2] - zlims[1]) < 1e-6 ]

    directions = ['x', 'y', 'z']
    limits = [xlims, ylims, zlims]
    surfaces_limits = [surfaces_x0, surfaces_xL, 
                       surfaces_y0, surfaces_yL, 
                       surfaces_z0, surfaces_zL]
    ph_list = {}
    for i, direction in enumerate(directions):
        for j, limit in enumerate(['0', 'L']):
            surfaces = surfaces_limits[2*i + j]
            name = f"{label}_{direction}{limit}"
            name_nolabel = f"{direction}{limit}"
            surf_obj = [s["surface"] for s in surfaces]
            ph = gmsh.model.addPhysicalGroup(2, surf_obj, -1)
            gmsh.model.setPhysicalName(2, ph, name)
            ph_list[name_nolabel] = surf_obj


    return ph_list

