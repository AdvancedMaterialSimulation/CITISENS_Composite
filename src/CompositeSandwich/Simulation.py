import os
join = os.path.join
from djccx.inp.inp import inp
import numpy as np

def Simulation(params):

    r = params["mesh"]["r"]
    results = params["mesh"]["results"]

    inp_f = inp(params["mesh"]["inp_file"])
    inp_f.remove_by_type(1)
    inp_f.remove_by_type(2)

    ylen = inp_f.nodes.df["y"].max() - inp_f.nodes.df["y"].min()
    epsilon = params["epsilon"]
    params["displ"] = epsilon*ylen

    for nset in results.keys():
        inp_f.CreateNsetFromIds(results[nset], nset)


    for inset in inp_f.nsets:
        df_0 = inset.GetNodes(inp_f.nodes)
        df_0 = df_0.sort_values(by=["x", "y", "z"])
        inset.id_nodes = df_0.index


    y_min_nset = inp_f.select("Y_MIN","nset")
    y_max_nset = inp_f.select("Y_MAX","nset")
    #Y_MIN_WITHOUT_EGDES 

    # select the nodes id where x not be 0 or 2*r

    df_0 = y_min_nset.GetNodes(inp_f.nodes)
    id_nodes = df_0[ (df_0.x != 0) & (df_0.x != params["mesh"]["xlims"][1]) ].index.values.copy()

    Y_MIN_WITHOUT_EDGES = inp_f.CreateNsetFromIds(id_nodes, "Y_MIN_WITHOUT_EDGES")

    #Y_MAX_WITHOUT_EDGES

    df_0 = y_max_nset.GetNodes(inp_f.nodes)
    id_nodes = df_0[ (df_0.x != 0) & (df_0.x != params["mesh"]["xlims"][1]) ].index.values.copy()

    Y_MAX_WITHOUT_EDGES = inp_f.CreateNsetFromIds(id_nodes, "Y_MAX_WITHOUT_EDGES")



    boxs_solid  = inp_f.select_regex(".*_BOX","elset")
    yarns_solid = inp_f.select_regex(".*YARN_.*","elset")
    box_mid     = inp_f.select("BOX_MID","elset")
    inp_f.AddEquation("X_MIN","X_MAX",dims=[1,2,3])


    young = params["materials"]["matrix"]["E"]
    nu    = params["materials"]["matrix"]["nu"]

    matrix_material = inp_f.CreateElasticMaterial("matrix",young,nu)

    young = params["materials"]["carbon"]["E"]
    nu    = params["materials"]["carbon"]["nu"]

    carbon_material = inp_f.CreateElasticMaterial("carbon",young,nu)

    allelset  = inp_f.CreateElsetAll()

    # inp_f.CreateSolidSection(box_solid,matrix_material)
    # inp_f.CreateSolidSection(yarn_solid_1,carbon_material)
    # inp_f.CreateSolidSection(yarn_solid_2,carbon_material)
    [ inp_f.CreateSolidSection(box,matrix_material) for box in boxs_solid ]
    [ inp_f.CreateSolidSection(yarn,carbon_material) for yarn in yarns_solid ]
    inp_f.CreateSolidSection(box_mid,matrix_material)
    # ============================================
    # STEP
    # ============================================

    displ_span = np.linspace(0,params["displ"],params["nsteps"])

    for i in range(len(displ_span)):
        istep = inp_f.CreateStaticStep(nlgeom=True)

        istep.CreateBoundary(Y_MIN_WITHOUT_EDGES,dim=2,displ=0)
        istep.CreateBoundary(Y_MAX_WITHOUT_EDGES,dim=2,displ=displ_span[i])


    output_folder = join(params["output"])

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frd = inp_f.run(output_folder)

    return frd