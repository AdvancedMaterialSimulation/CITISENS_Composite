import os
join = os.path.join
from djccx.inp.inp import inp

def Simulation(results,r):

    inp_f = inp("composite_pbc_min.inp")
    inp_f.remove_by_type(1)
    inp_f.remove_by_type(2)


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
    id_nodes = df_0[ (df_0.x != 0) & (df_0.x != 2*r) ].index.values.copy()

    Y_MIN_WITHOUT_EDGES = inp_f.CreateNsetFromIds(id_nodes, "Y_MIN_WITHOUT_EDGES")

    #Y_MAX_WITHOUT_EDGES

    df_0 = y_max_nset.GetNodes(inp_f.nodes)
    id_nodes = df_0[ (df_0.x != 0) & (df_0.x != 2*r) ].index.values.copy()

    Y_MAX_WITHOUT_EDGES = inp_f.CreateNsetFromIds(id_nodes, "Y_MAX_WITHOUT_EDGES")


    yarn_solid_1 = inp_f.select("YARN_1","elset")
    yarn_solid_2 = inp_f.select("YARN_2","elset")
    box_solid    = inp_f.select("BOX","elset")


    inp_f.AddEquation("X_MIN","X_MAX",dims=[1,2,3])


    young = 2960
    nu = 0.3
    matrix_material = inp_f.CreateElasticMaterial("matrix",young,nu)

    young = 2000000
    nu = 0.3
    carbon_material = inp_f.CreateElasticMaterial("carbon",young,nu)

    allelset  = inp_f.CreateElsetAll()

    inp_f.CreateSolidSection(box_solid,matrix_material)
    inp_f.CreateSolidSection(yarn_solid_1,carbon_material)
    inp_f.CreateSolidSection(yarn_solid_2,carbon_material)

    # ============================================
    # STEP
    # ============================================
    istep = inp_f.CreateStaticStep(nlgeom=True)

    istep.CreateBoundary(Y_MIN_WITHOUT_EDGES,dim=2,displ=0.0)
    istep.CreateBoundary(Y_MAX_WITHOUT_EDGES,dim=2,displ=1.0)


    inflation_folder = join("output")

    if not os.path.exists(inflation_folder):
        os.makedirs(inflation_folder)

    frd = inp_f.run(inflation_folder)

    return frd