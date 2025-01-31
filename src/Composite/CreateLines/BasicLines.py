from .layers import LayerX, LayerY
from .LayerSinX import LayerSinX
from .LayerSinY import LayerSinY
from .LayerSinX_smooth import LayerSinX_smooth
from .LayerSinY_smooth import LayerSinY_smooth

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
    trajs_SX_smooth = LayerSinX_smooth(**S_params)
    trajs_SY_smooth = LayerSinY_smooth(**S_params)

    return {
        "trajs_X": trajs_X,
        "trajs_Y": trajs_Y,
        "trajs_SX": trajs_SX,
        "trajs_SY": trajs_SY,
        "trajs_SX_smooth": trajs_SX_smooth,
        "trajs_SY_smooth": trajs_SY_smooth,
        "Lx": Lx,
        "Ly": Ly
    }