
from copy import deepcopy
from .is_semicylinder_mesh import is_semicylinder_mesh
from .semicylinder_mesh import semicylinder_mesh
from .cutgeo import cutgeo

from functions.CreateYarnInterface import CreateYarn
import os
import numpy as np

SET_DESIGNS = ["A","B","C","D","E","F"]

def CreateYarns(params,output_folder):


    radius = params["r"]
    trajs_layers = params["trajs_layers"]
    trajs_layers = [ trajs_layers[key] for key in trajs_layers.keys()]
    h = params["h"]
    z0 = params["z0"]
    Lx = params["Lx"]
    Ly = params["Ly"]
    mirror = params["mirror"]
    interface_factor = params["interface_factor"]
    density = params["density"]
    names =["minus","plus"]
    with_interface = params["with_interface"]

    for k,isign in enumerate([-1,1]):
        if mirror and isign == -1:
            continue
        for j,trajs in enumerate(trajs_layers):
            
            for i,itraj in enumerate(trajs):
                itraj = deepcopy(itraj)
                itraj = np.array(itraj)
                itraj[:,2] = itraj[:,2] + isign*(h*j + z0)
                file = "layer_{}_yarn_{}_{}.brep".format(j+1,i+1,names[k])
                file = os.path.join(output_folder,file)
                
                if with_interface:
                    file_radius = [ "r.brep", "r1_25.brep"]
                    radius_valu = [radius,interface_factor*radius]

                    for iradius,ifile in zip(radius_valu,file_radius):
                        
                        if is_semicylinder_mesh(itraj,Lx,Ly):
                            semicylinder_mesh(itraj, iradius, ifile)
                        else:
                            CreateYarn({"trajs": itraj, 
                                        "radius": iradius, 
                                        "density": density,
                                        "Lx": Lx,
                                        "Ly": Ly,
                                        "file": ifile})
                        
                    cutgeo(file_radius[0],file_radius[1],file)
                        # rm file
                    os.system("rm -f {}".format(file_radius[0]))
                    os.system("rm -f {}".format(file_radius[1]))
                
                else:
                    
                    if is_semicylinder_mesh(itraj,Lx,Ly):
                        semicylinder_mesh(itraj, radius, file)
                    else:
                        CreateYarn({"trajs": itraj, 
                                    "radius": radius, 
                                    "density": density,
                                    "Lx": Lx,
                                    "Ly": Ly,
                                    "file": file})
                    
            print("Layer With Sign {} and number {}/{} done".format(isign,j+1,len(trajs_layers)))

    return params