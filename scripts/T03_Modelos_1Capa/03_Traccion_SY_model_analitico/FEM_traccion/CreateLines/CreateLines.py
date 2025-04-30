from .BasicLines import BasicLines
def CreateLines(params):

    # ==================

    trajs_basic = BasicLines(params)
    trajs_X  = trajs_basic["trajs_X"]
    trajs_Y  = trajs_basic["trajs_Y"]
    trajs_SX = trajs_basic["trajs_SX"]
    trajs_SY = trajs_basic["trajs_SY"]
    # 
    Lx = trajs_basic["Lx"]
    Ly = trajs_basic["Ly"]


    designs = {"X" : [trajs_X],
               "Y" : [trajs_Y],
               "SX": [trajs_SX],
               "SY": [trajs_SY],
                }
    
    # list to dict
    
    for key in designs.keys():
        designs[key] = {"ly_"+str(i):designs[key][i] 
                        for i in range(len(designs[key]))}

    params["designs"] = designs
    params["Lx"] = Lx
    params["Ly"] = Ly
    params["longs"] = trajs_basic["longs"]
    
    return params