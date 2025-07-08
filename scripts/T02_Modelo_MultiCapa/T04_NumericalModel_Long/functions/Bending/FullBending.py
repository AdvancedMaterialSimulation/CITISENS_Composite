from  .CreateGeoBending import CreateGeoBending
from  .SimulationBending import SimulationBending
from AnalyticalLayers.models import E_flexion,E_Tensile
from .PostProcessingBending import PostProcessingBending
import numpy as np
import os 
from djccx.inp.inp import inp
from djccx.frd.readfrd import readfrd

join = os.path.join

def FullBending(params):

    output_folder = params["output_folder"]

    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)

    geo_folder = join(output_folder,"geo")
    sim_folder = join(output_folder,"sim")


    params["geo"]["n_l"] = len(params["sim"]["E_l"])
    params["geo"]["output_folder"] = geo_folder
    # mkdir if not exist
    if os.path.exists(geo_folder) == False:
        os.mkdir(geo_folder)

    file_geo = os.path.join(geo_folder,"composite_layers.inp")
    if os.path.exists(file_geo):
        params["geo"]["t_t"] = 2*params["geo"]["t_l"]*params["geo"]["n_l"] + \
                          params["geo"]["t_n"]
        print(f"Geo file {file_geo} already exists. Skipping geometry creation.")
    else:
        CreateGeoBending(params["geo"])

    params["sim"]["t_t"] = params["geo"]["t_t"]


    params["sim"]["output_folder"] = sim_folder
    # mkdir if not exist
    if os.path.exists(sim_folder) == False:
        os.mkdir(sim_folder)

    file_sim = os.path.join(sim_folder,"main.inp")
    if os.path.exists(file_sim):
        print(f"Simulation file {file_sim} already exists. Skipping simulation creation.")
        inp_f = inp(file_sim)
        ifrd  = readfrd(join(sim_folder,"main.frd"))
    else:
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



    layers = params["sim"]["name_mat"]
    tn = params["geo"]["t_n"]
    tl = params["geo"]["t_l"]
    En = params["sim"]["E_n"]
    # factor de correccion de 0.8 para el Eflexion
    params["Eflexion_analytical"] = E_flexion(1e-3*En,params["El"],tn,tl,layers)

    params["Etensile_analytical"] = E_Tensile(1e-3*En,params["El"],tn,tl,layers)




    return inp_f