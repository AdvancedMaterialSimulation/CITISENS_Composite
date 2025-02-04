from djccx.inp.inp import inp
from Composite.inp.CreateNsetFromElset import CreateNsetFromElset
import os
join = os.path.join
def SimulationBending(params):

    # inp_f = inp("../geo/composite_layers.inp")
    inp_f = inp(join(params["output_folder"],
                        "..",
                        "geo",
                        "composite_layers.inp"))

    t_t = params["t_t"]
    E_l = params["E_l"]
    E_n = params["E_n"]
    disp = params["disp"]
    output = params["output_folder"]


    elset_symmetry = inp_f.select("SYMMETRY","elset")
    nset_symmetry = CreateNsetFromElset(inp_f, elset_symmetry, "nset_symmetry")

    # select all nodes that have x=Lx and z=0
    df_nodes = inp_f.nodes.df
    eps = 1e-3

    sel_egdes = lambda x,z: df_nodes[(df_nodes["x"] > x - eps) &\
                                    (df_nodes["x"] < x + eps) &\
                                    (df_nodes["z"] > z - eps) &\
                                    (df_nodes["z"] < z + eps)].index


    Lx = inp_f.nodes.df["x"].max()
    nid = sel_egdes(Lx,-t_t/2)
    nset_fixed = inp_f.CreateNsetFromIds(nid, "nset_fixed")

    nid = sel_egdes(0,t_t/2)
    nset_load = inp_f.CreateNsetFromIds(nid, "nset_load")
    #
    # remove 1d 2d elements
    inp_f.remove_by_type(1)
    inp_f.remove_by_type(2)

    elset_all = inp_f.CreateElsetAll()
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

    layer_sel = lambda i: inp_f.select_regex("LAYER_{}.*".format(i),"elset")
    for i, iEs in enumerate(E_l):
        for ielset in layer_sel(i+1):
            inp_f.CreateSolidSection(ielset,materials[i])

    istep = inp_f.CreateStaticStep()
    # 

    istep.CreateBoundary(nset_symmetry,1,0.0)
    istep.CreateBoundary(nset_fixed,3,0.0)
    istep.CreateBoundary(nset_load,3,-disp)

    # create output if not exist
    if os.path.exists(output) == False:
        os.mkdir(output)
    ifrd = inp_f.run(output)
    
    

    return inp_f,ifrd