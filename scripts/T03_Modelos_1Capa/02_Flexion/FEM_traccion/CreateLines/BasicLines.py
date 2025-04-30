from .layers import LayerX, LayerY
from .LayerSinX import LayerSinX
from .LayerSinY import LayerSinY

import numpy as np
def BasicLines(params):

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

    r =  {
        "trajs_X": trajs_X,
        "trajs_Y": trajs_Y,
        "trajs_SX": trajs_SX,
        "trajs_SY": trajs_SY,
        "Lx": Lx,
        "Ly": Ly
    }

    # Calculamos las longitudes de cada una de la capas de diseño 
    trajs_keys = [ i for i in r.keys() if "trajs" in i]
    longs = [ np.sum([ np.sum( np.sqrt( (c[1:]-c[:-1])**2 ) ) 
             for c in r[itrajs_keys] ] ) 
             for itrajs_keys in trajs_keys]

    r["longs"] = {itrajs_keys:longs[i] for i,itrajs_keys in enumerate(trajs_keys)}

    return r