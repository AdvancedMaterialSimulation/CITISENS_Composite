from .layers import LayerX, LayerY
from .LayerSinX import LayerSinX
from .LayerSinY import LayerSinY
import numpy as np
def CreateLines(params):

    Nx_sq = params["Nx_sq"]
    Ny_sq = params["Ny_sq"]
    r     = params["r"]
    type = params["type"]
    # ==================
    Nx_sq_db = 2*Nx_sq
    Ny_sq_db = 2*Ny_sq

    Nx = 3*Nx_sq_db
    Ny = 3*Nx_sq_db

    Lx = 2*r*Nx_sq_db
    Ly = 2*r*Ny_sq_db

    trajs_X = LayerX(Lx, Ly, Nx)
    trajs_Y = LayerY(Lx, Ly, Ny)

    S_params = {'Nx'  : Nx_sq_db,
                'Ny'  : Ny_sq_db,
                'type': type,
                "r"   : r}

    trajs_SX = LayerSinX(**S_params) 
    trajs_SY = LayerSinY(**S_params)

    # Patrones de diseño
    design_A = [trajs_X]
    design_B = [trajs_X,trajs_Y]
    design_C = [trajs_X,trajs_SX]
    design_D = [trajs_X,trajs_SY]
    design_E = [trajs_X,trajs_SY,trajs_SX]
    design_F = [trajs_X,trajs_Y,trajs_SY,trajs_SX]

    design_B1 = [trajs_Y]
    

    designs = {"A" : design_A,
               "B" : design_B,
               "C" : design_C,
               "D" : design_D,
               "E" : design_E,
               "F" : design_F,
               "B1": design_B1}
    
    # list to dict
    
    for key in designs.keys():
        designs[key] = {"ly_"+str(i):designs[key][i] 
                        for i in range(len(designs[key]))}

    params["designs"] = designs
    params["Lx"] = Lx
    params["Ly"] = Ly
    
    return params