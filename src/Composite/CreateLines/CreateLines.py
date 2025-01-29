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