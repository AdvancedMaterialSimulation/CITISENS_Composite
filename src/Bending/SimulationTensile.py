from djccx.inp.inp import inp
from Composite.inp.CreateNsetFromElset import CreateNsetFromElset
import os
join = os.path.join
import numpy as np

def SimulationTensile(params):

    # inp_f = inp("../geo/composite_layers.inp")
    inp_f = inp(join(params["output_folder"],
                        "..",
                        "geo",
                        "composite_layers.inp"))

    # t_t = params["t_t"]
    E_l = params["E_l"]
    E_n = params["E_n"]
    disp = params["disp"]
    output = params["output_folder"]


    # elset_symmetry = inp_f.select("SYMMETRY","elset")
    # nset_symmetry = CreateNsetFromElset(inp_f, elset_symmetry, "nset_symmetry")

    # select all nodes that have x=Lx and z=0
    # df_nodes = inp_f.nodes.df
    # eps = 1e-3

    # ========================================================
    YL_elsets = inp_f.select_regex(".*YL","elset")
    YL_nsets = []
    for i,ielset in enumerate(YL_elsets):
        nset = CreateNsetFromElset(inp_f,ielset,"NSET_YL_{}".format(i+1))
        YL_nsets.append(nset)

    YL_nset = inp_f.CreateNsetFromNsets("NSET_YL",YL_nsets)

    Y0_elsets = inp_f.select_regex(".*Y0","elset")
    Y0_nsets = []

    for i,ielset in enumerate(Y0_elsets):
        nset = CreateNsetFromElset(inp_f,ielset,"NSET_Y0_{}".format(i+1))
        Y0_nsets.append(nset)

    Y0_nset = inp_f.CreateNsetFromNsets("NSET_Y0",Y0_nsets)

    # ========================================================
    XL_elsets = inp_f.select_regex(".*XL","elset")
    XL_nsets = []
    for i,ielset in enumerate(XL_elsets):
        nset = CreateNsetFromElset(inp_f,ielset,"NSET_XL_{}".format(i+1))
        XL_nsets.append(nset)

    XL_nset = inp_f.CreateNsetFromNsets("NSET_XL",XL_nsets)

    X0_elsets = inp_f.select_regex(".*X0","elset")
    X0_nsets = []

    for i,ielset in enumerate(X0_elsets):
        nset = CreateNsetFromElset(inp_f,ielset,"NSET_X0_{}".format(i+1))
        X0_nsets.append(nset)

    X0_nset = inp_f.CreateNsetFromNsets("NSET_X0",X0_nsets)


    # ========================================================

    # sel_egdes = lambda x,z: df_nodes[(df_nodes["x"] > x - eps) &\
    #                                 (df_nodes["x"] < x + eps) &\
    #                                 (df_nodes["z"] > z - eps) &\
    #                                 (df_nodes["z"] < z + eps)].index


    # Lx = inp_f.nodes.df["x"].max()
    # nid = sel_egdes(Lx,-t_t/2)
    # nset_fixed = inp_f.CreateNsetFromIds(nid, "nset_fixed")

    # nid = sel_egdes(0,t_t/2)
    # nset_load = inp_f.CreateNsetFromIds(nid, "nset_load")
    #
    # remove 1d 2d elements
    inp_f.remove_by_type(1)
    inp_f.remove_by_type(2)

    # elset_all = inp_f.CreateElsetAll()
    # 

    materials = []
    nu = 0.4
    for i,iEs in enumerate(E_l):
        name_mat = "mat_{}".format(i+1)
        name_mat = params["name_mat"][i] + "_{}".format(i+1)
        materials.append(inp_f.CreateElasticMaterial(name_mat, iEs, nu))

    mat_nucleo   = inp_f.CreateElasticMaterial("mat_nucleo", E_n, nu)
    elset_nucleo = inp_f.select("NUCLEO","elset")
    inp_f.CreateSolidSection(elset_nucleo,mat_nucleo)

    #layer_sel = lambda i: inp_f.select_regex("LAYER_{}.*".format(i),"elset")

    def layer_sel(i):
        r =  inp_f.select_regex("LAYER_{}.*".format(i),"elset")
        # 
        cp = ["MINUS","PLUS"]
        # must be contained in the name
        r = [i for i in r if cp[0] in i.name or cp[1] in i.name ]
        return r

    for i, iEs in enumerate(E_l):
        layers = layer_sel(i+1)
        for ielset in layers:
            inp_f.CreateSolidSection(ielset,materials[i])


    disp_span = np.linspace(0,disp,4)
    for disp in disp_span:
        istep = inp_f.CreateStaticStep()
        # 
        istep.CreateBoundary(Y0_nset,2,0.0)
        istep.CreateBoundary(YL_nset,2,disp)

        # istep.CreateBoundary(X0_nset,1,0.0)
        # istep.CreateBoundary(XL_nset,1,0.0)

    # create output if not exist
    if os.path.exists(output) == False:
        os.mkdir(output)
    ifrd = inp_f.run(output,opt=params["opt"])
    
    

    return inp_f,ifrd