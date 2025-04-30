import os,shutil
from .CreateYarns.CreateYarns import CreateYarns
from .CreateBoxMirror.CreateBoxMirror import CreateBoxMirror

fc_mesh_max_d = {
    "X"       : 1.0,
    "Y"       : 1.0,
    "SX"      : 1.0,
    "SY"      : 1.0

}
fc_mesh_min_d = {
    "X"      : 0.35,
    "Y"      : 0.35,
    "SX"     : 0.30,
    "SY"     : 0.35
}


def GenerateMeshRVE(lines,select_design,output_folder,params_composite):

    output_folder = os.path.join(output_folder,select_design)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    params_composite["trajs_layers"] = lines["designs"][select_design]
    
    params_composite["fc_mesh_min"] = fc_mesh_min_d[select_design]
    params_composite["fc_mesh_max"] = fc_mesh_max_d[select_design]

    params_composite["Lx"] = lines["Lx"]
    params_composite["Ly"] = lines["Ly"]
    params_composite["select_design"] = select_design

    output_folder = output_folder.split(os.sep)
    # ==========================================================
    # 1. Create the Yarn Geometry
    # ==========================================================
    CreateYarns(params_composite,os.path.join(*output_folder))

    # ==========================================================
    # 2. Create the Box, load yarns and create the mesh
    CreateBoxMirror(params_composite,output_folder)
    # ==========================================================
 
    return params_composite