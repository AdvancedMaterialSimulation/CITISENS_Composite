from Bending.CreateGeoBending import CreateGeoBending
from Bending.SimulationBending import SimulationBending
from Bending.SimulationTensile import SimulationTensile
from AnalyticalLayers.models import E_flexion, E_Tensile,Rotura,RoturaBending
from .PostProcessingTensile import PostProcessingTensile
from .PostProcessingBending import PostProcessingBending
import numpy as np
import os 

join = os.path.join

def FullBending(params):

    output_folder = params["output_folder"]

    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)

    geo_folder = join(output_folder,"geo")
    sim_folder = join(output_folder,"sim")
    tensile_folder = join(output_folder,"tensile")


    params["geo"]["n_l"] = len(params["sim"]["E_l"])
    params["geo"]["output_folder"] = geo_folder
    # mkdir if not exist
    if os.path.exists(geo_folder) == False:
        os.mkdir(geo_folder)
    CreateGeoBending(params["geo"])

    params["sim"]["t_t"] = params["geo"]["t_t"]


    params["sim"]["output_folder"] = sim_folder
    # mkdir if not exist
    if os.path.exists(sim_folder) == False:
        os.mkdir(sim_folder)

    inp_f,ifrd = SimulationBending(params["sim"])


    data = ifrd["data"]

    F3 = data["F3"][data["x"] < np.mean(data["x"])]

    P = -2*np.sum(F3) # 2 because it is a half model
    U = params["sim"]["disp"]
    L = 2*params["geo"]["Lx"]
    B = params["geo"]["Ly"]
    t = params["geo"]["t_t"]

    params["Eflex"] = (P*L**3)/(4*U*B*t**3) * 1e-3
    params["Force"] = P
    # 



    params["rpostbending"] = PostProcessingBending({
        "composition": params["sim"]["name_mat"],
        "tt"         : t,
        "St_layers"  : params["tensile"]["St_layers"],
        "inp_f"      : inp_f,
        "ifrd"       : ifrd,
        "geo"        : params["geo"]
    })

    params["sim"]["output_folder"] = tensile_folder

    params["sim"]["disp"] = params["tensile"]["disp"]
    inp_f,ifrd = SimulationTensile(params["sim"])

    data = ifrd["data"]
    disp = params["sim"]["disp"]

    epsilon = disp/params["geo"]["Ly"]
    F2 = data["F2"][data["y"] > np.mean(data["y"])]
    F2 = np.sum(F2)
    Lx = params["geo"]["Lx"] 
    A_t = Lx*t

    sigma = F2/A_t

    E_eff = sigma/epsilon
    params["Etensile"] = E_eff * 1e-3


    layers = params["sim"]["name_mat"]
    tn = params["geo"]["t_n"]
    tl = params["geo"]["t_l"]
    En = params["sim"]["E_n"]
    # factor de correccion de 0.8 para el Eflexion
    params["Eflexion_analytical"] = 0.8*E_flexion(1e-3*En,params["El"],tn,tl,layers)
    nu = 0.3
    # params["Eflexion_analytical"] = params["Eflexion_analytical"] * (1 - nu**2)

    params["Etensile_analytical"] = E_Tensile(1e-3*En,params["El"],tn,tl,layers)

    Et_eff = params["Etensile_analytical"]
    Ef_eff = params["Eflexion_analytical"]
    sigmal = [ params["tensile"]["St_layers"][il] 
              for il in ["X","SX","Y","SY"]]
    
    params["St_analytical"] = Rotura(layers,
                                     1e-3*Et_eff,
                                     params["El"],
                                     sigmal)

    params["Sb_analytical"] = RoturaBending(layers,
                                            1e-3*Ef_eff,
                                            params["El"],
                                            sigmal,
                                            tn,
                                            tl)

    rpost = PostProcessingTensile({
        "composition" :  params["sim"]["name_mat"],
        "Lx"          :  params["geo"]["Lx"],
        "tn"          :  params["geo"]["t_n"],
        "tt"          :  params["geo"]["t_t"],
        "St_layers"   :  params["tensile"]["St_layers"],
        "inp_f"       :  inp_f,
        "ifrd"        :  ifrd,
        "tl"          :  params["geo"]["t_l"]
    })

    params["rpost"] = rpost




    return inp_f