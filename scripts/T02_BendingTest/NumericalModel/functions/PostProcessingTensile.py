import numpy as np 
composition = [
        ["Y", "Y"],
        ["Y", "X"],
        ["Y", "SX"],
        ["Y", "SY"],
        ["Y", "SX" , "SY"],
        ["Y", "X"  , "SY"]
    ]

def PostProcessingTensile(params):

    composition = params["composition"]
    Lx = params["Lx"]
    tn = params["tn"]
    tt = params["tt"]
    St_layers = params["St_layers"]
    inp_f = params["inp_f"]
    ifrd = params["ifrd"]
    tl = params["tl"]
    # ========================

    LAYERS =  inp_f.elements

    YLs = inp_f.select_regex(".*YL_.*","nset")
    icomp = [ *composition[::-1] , "nucleo", *composition ]

    ti = np.array([tl for i in range(len(icomp))])
    ti[len(icomp)//2] = tn

    A = ti*Lx
    print(icomp)

    rr = []
    for data in ifrd["data_blocks"]:
        F2s = []
        S2s = []
        
        # ========================
        # Principal Stress
        # ========================
        P1s = []

        for idx in range(len(LAYERS)):
            nodes = LAYERS[idx].GetUniqueNodes(inp_f.nodes)
            y = nodes["y"]

            # =================================
            # query the middle of the layer y 
            ymin = y.min()
            ymax = y.max() 
            yL = ymax - ymin
            ymin_new = y.min() + yL/3
            ymax_new = y.max() - yL/3
            nodes = nodes[(nodes["y"]>ymin_new) & (nodes["y"]<ymax_new)]
            # query the middle of the layer z
            z = nodes["z"]
            zunq = np.unique(z)
            zmean = np.mean(zunq)
            znear = np.argmin(np.abs(zunq - zmean))
            z = zunq[znear]
            nodes =  nodes[nodes["z"] == z]
            # ==================================

            P1max = np.max(data.loc[nodes.index]["P1"])
            P1s.append(P1max)

        P1s = np.array(P1s)
        # ========================
        # Force By layers
        # ========================
        
        for idx in range(len(YLs)):
            df = data.loc[YLs[idx].id_nodes]
            F2 = df["F2"].sum()
            F2s.append(F2)
            S2 = F2/A[idx]
            S2s.append(S2)

        S2s = np.array(S2s)
        # ========================
        # Total Force
        # ========================

        F2 = data["F2"]
        y = data["y"]
        A_ly1 = Lx*tt
        F2_tot = F2[y>y.mean()].sum()
        sigma_tot = F2_tot.sum()/A_ly1

        r = { 
            "Sapl_by_layers" : S2s,
            "Sapl" : sigma_tot,
            "layers" : icomp,
            "P1" : P1s,
        }
        rr.append(r)

    Sapl_time = [ r["Sapl"] for r in rr ]
    
    ly = len(LAYERS)

    Ls = [ ]
    for i in range(ly):
        Ls.append([ r["Sapl_by_layers"][i] for r in rr ])

    P1s =[]
    for i in range(ly):
        P1s.append([ r["P1"][i] for r in rr ])

    ly = len(LAYERS)
    P1s_end = [ P1[-1] for P1 in P1s ]
    P1s_end = np.array(P1s_end)
    P1s_end = P1s_end[ : ly%2 +1  ]

    sigma_an =  [ St_layers[ly] for ly in icomp[:ly%2 +1 ] ]

  
    S_prediction = np.min( (Sapl_time[-1]/ P1s_end)*sigma_an )


    return {
        "Sapl_time" : Sapl_time,
        "Sapl_layers" : Ls,
        "Sapl_layers_end" : P1s_end,
        "Sapl_layers_an" : sigma_an,
        "S_prediction" : S_prediction,
    }

