
from copy import deepcopy
from .is_semicylinder_mesh import is_semicylinder_mesh
from .semiellipse_mesh import semiellipse_mesh

from functions.CreateYarnElipse import CreateYarnElipse
import os
import numpy as np

SET_DESIGNS = ["A","B","C","D","E","F"]

def CreateYarns(params,output_folder):


    radius = params["r"]
    trajs_layers = params["trajs_layers"]
    trajs_layers = [ trajs_layers[key] for key in trajs_layers.keys()]
    h = params["h"]
    z0 = params["z0"] + h/2
    Lx = params["Lx"]
    Ly = params["Ly"]
    density = params["density"]
    names =["minus","plus"]

    factor_radius = params["factor_radius"]

    for k,isign in enumerate([-1,1]):
        if True and isign == -1:
            continue
        for j,trajs in enumerate(trajs_layers):
            
            for i,itraj in enumerate(trajs):
                itraj = deepcopy(itraj)
                itraj = np.array(itraj)
                itraj[:,2] = itraj[:,2] + isign*(h*j + z0)
                file = "layer_{}_yarn_{}_{}.brep".format(j+1,i+1,names[k])
                file = os.path.join(output_folder,file)
                
                if is_semicylinder_mesh(itraj,Lx,Ly):
                    #semicylinder_mesh(itraj, radius/factor_radius, file)
                    semiellipse_mesh(itraj, radius, file,factor_radius)
                else:
                    CreateYarnElipse({"trajs": itraj, 
                                "radius": radius, 
                                "density": density,
                                "Lx": Lx,
                                "Ly": Ly,
                                "factor_radius": factor_radius,
                                "file": file})
                
            print("Layer With Sign {} and number {}/{} done".format(isign,j+1,len(trajs_layers)))

    return params