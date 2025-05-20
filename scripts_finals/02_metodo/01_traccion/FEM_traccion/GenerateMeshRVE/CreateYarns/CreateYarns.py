
from copy import deepcopy
from .functions.is_semicylinder_mesh import is_semicylinder_mesh
from .functions.semiellipse_mesh import semiellipse_mesh
from .functions.CreateYarn import CreateYarn

import os
import numpy as np

def CreateYarns(params,output_folder):

    trajs_layers = params["trajs_layers"]
    trajs_layers = [ trajs_layers[key] 
                    for key in trajs_layers.keys()]
    
    radius  = params["r"]
    h       = params["h"]
    z0      = params["z0"] + h/2
    Lx      = params["Lx"]
    Ly      = params["Ly"]
    density = params["density"]

    layers = params["designs_str"][params["select_design"]]

    d_all = params["d"]

    
    for j,trajs in enumerate(trajs_layers):
        
        d = d_all[layers[j]]
        for i,itraj in enumerate(trajs):

            itraj = deepcopy(itraj)
            itraj = np.array(itraj)
            
            itraj[:,2] = itraj[:,2] + (h*j + z0)

            file = "layer_{}_yarn_{}.brep".format(j+1,i+1)
            file = os.path.join(output_folder,file)
            
            if is_semicylinder_mesh(itraj,Lx,Ly):

                semiellipse_mesh(itraj, 
                                 radius, 
                                 file,
                                 d)
            else:
                
                CreateYarn({  "trajs"         : itraj, 
                              "radius"        : radius, 
                              "density"       : density,
                              "Lx"            : Lx,
                              "Ly"            : Ly,
                              "d" : d,
                              "file"          : file})
            
        print("Layer number {}/{} done".format(j+1,len(trajs_layers)))

    return params