import numpy as np 
composition = [
        ["Y", "Y"],
        ["Y", "X"],
        ["Y", "SX"],
        ["Y", "SY"],
        ["Y", "SX" , "SY"],
        ["Y", "X"  , "SY"]
    ]
def PostProcessingBending(params):

    composition = params["composition"]
    tt = params["tt"]
    St_layers = params["St_layers"]
    inp_f = params["inp_f"]
    ifrd = params["ifrd"]

    LAYERS =  inp_f.elements

    B = params["geo"]["Ly"]

    icomp = [ *composition[::-1] , "nucleo", *composition ]

    print(icomp)

    rr = []
    L = 2*params["geo"]["Lx"]

    for it,data in enumerate(ifrd["data_blocks"]):
        
        # ========================
        # Principal Stress
        # ========================
        P1s = []
        print("Time Step:")

        for idx in range(len(LAYERS)):
            nodes = LAYERS[idx].GetUniqueNodes(inp_f.nodes)

            zmin_to_eval = nodes["z"].min()

            x0 = 0
            y0 = B/2
            eps = 0.1

            nodes = nodes[nodes["x"] > x0 - eps]
            nodes = nodes[nodes["x"] < x0 + eps]
            nodes = nodes[nodes["y"] > y0 - eps]
            nodes = nodes[nodes["y"] < y0 + eps]
            
            zmax = nodes["z"].max()
            zmin = nodes["z"].min()
            zlen = zmax - zmin
            factor = 0.1
            zmin_new = zmin + factor*zlen
            zmax_new = zmax - factor*zlen

            nodes = nodes[nodes["z"] > zmin_new]
            nodes = nodes[nodes["z"] < zmax_new]
            # linear regression
            
            P1 = data.loc[nodes.index]["P1"]
            nodes["P1"] = P1

            # linear regression z vs P1
            z_reg  = nodes["z"]
            P1_reg = nodes["P1"]

            A = np.vstack([z_reg, np.ones(len(z_reg))]).T
            m, c = np.linalg.lstsq(A, P1_reg, rcond=None)[0]
            
            P1_reg = m*zmin_to_eval + c

            if it != 0:
                P1s.append(P1_reg)
            else:
                P1s.append(0)

        P1s = np.array(P1s)
        
        nodes = inp_f.nodes
        NSET_LOAD = inp_f.select("NSET_LOAD","nset")
        NSET_LOAD.GetNodes(inp_f.nodes)
        F3 = data.loc[NSET_LOAD.GetNodes(inp_f.nodes).index]["F3"]
        F3 = -2*np.sum(F3) # Symmetry of Model

        # force
        B = params["geo"]["Ly"]
        D = tt
        L = 2*params["geo"]["Lx"]

        #
        # Medimos la fuerza en la mitad del modelo 
        # y calculamos la transformación a la fuerza que se aplican en los datos experimentales
        #
        sigma_exp = (3/2)*F3*L/(B*D**2)

        r = { 
            "layers" : icomp,
            "P1" : P1s,
            "F3" : F3,
            "sigma_exp" : sigma_exp
        }
        rr.append(r)
    
    ly = len(LAYERS)

    P1s =[]
    for i in range(ly):
        P1s.append([ r["P1"][i] for r in rr ])

    S3s = [ r["sigma_exp"] for r in rr ]

    ly = len(LAYERS)
    P1s_end = [ P1[-1] for P1 in P1s ]
    P1s_end = np.array(P1s_end)
    P1s_end = P1s_end[ : ly%2 +1  ]

    alpha = P1s_end/S3s[-1]

    sigma_an =  [ St_layers[ly] for ly in icomp[:ly%2 +1 ] ]
    sigma_an = np.array(sigma_an)

    S3_pred = np.min(sigma_an/alpha)
    
    return S3_pred