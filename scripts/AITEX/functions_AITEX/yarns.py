
from copy import deepcopy
from functions_AITEX.is_semicylinder_mesh import is_semicylinder_mesh
from functions_AITEX.semicylinder_mesh import semicylinder_mesh
from functions.CreateYarnInterface import CreateYarn
from functions_AITEX.cutgeo import cutgeo
import os
def yarns(params):
    radius = params["r"]
    trajs_layers = params["trajs_layers"]
    h = params["h"]
    z0 = params["z0"]
    Lx = params["Lx"]
    Ly = params["Ly"]
    interface_factor = params["interface_factor"]
    density = params["density"]
    names =["minus","plus"]
    with_interface = params["with_interface"]

    for k,isign in enumerate([-1,1]):
        for j,trajs in enumerate(trajs_layers):

            for i,itraj in enumerate(trajs):
                itraj = deepcopy(itraj)
                itraj[:,2] = itraj[:,2] + isign*(h*j + z0)
                file = "output/mesh/layer_{}_yarn_{}_{}.brep".format(j+1,i+1,names[k])

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
                    print("file: ",file)
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
                    
                    print("file: ",file)