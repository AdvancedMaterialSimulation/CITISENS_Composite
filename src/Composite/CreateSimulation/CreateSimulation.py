from djccx.inp.inp import inp
from Composite.inp.CreateNsetFromElset import CreateNsetFromElset
from Composite.inp.CreateElsetFromElsets import CreateElsetFromElsets
from validation.experimental import carbonfiber,resina,nucleo
import os
import pandas as pd
from Composite.inp.are_coplanar import are_coplanar
import numpy as np
import shutil,sys,os

def CreateSimulation(design_folder,
                     output_folder,
                     params,
                     no_shell=True):

    inp_f = inp(os.path.join(design_folder,
                             "composite.inp"))
    
    PLANES = inp_f.select_regex(".*PLANE.*","elset")

    X0_PLANE = [ ip for ip in PLANES if "X0" in ip.name][0]
    Y0_PLANE = [ ip for ip in PLANES if "Y0" in ip.name][0]
    XL_PLANE = [ ip for ip in PLANES if "XL" in ip.name][0]
    YL_PLANE = [ ip for ip in PLANES if "YL" in ip.name][0]

    X0_PLANE_NSET = CreateNsetFromElset(inp_f,X0_PLANE,name="X0_PLANE")
    Y0_PLANE_NSET = CreateNsetFromElset(inp_f,Y0_PLANE,name="Y0_PLANE")
    XL_PLANE_NSET = CreateNsetFromElset(inp_f,XL_PLANE,name="XL_PLANE")
    YL_PLANE_NSET = CreateNsetFromElset(inp_f,YL_PLANE,name="YL_PLANE")

    PLUS_ZL_PLANE = inp_f.select("PLUS_ZL","elset")

    PLUS_ZL_PLANE_NSET = CreateNsetFromElset(inp_f,PLUS_ZL_PLANE,name="PLUS_ZL_PLANE")

    try:
        ALMA_Z0_PLANE = inp_f.select("ALMA_Z0","elset")
        ALMA_Z0_PLANE_NSET = CreateNsetFromElset(inp_f,ALMA_Z0_PLANE,name="ALMA_Z0_PLANE")
    except:
        pass

    inp_f.remove_by_type(1)
    # inp_f.remove_by_type(2)

    # SURFACE_ELSET = inp_f.select_regex(".*SURFACE.*","elset")
    # inp_f.cards = [ card for card in inp_f.cards if card.type != "*ELEMENT" ]
    yarns_elsets = inp_f.select_regex(".*YARN.*","elset")
    elset_yarns = CreateElsetFromElsets(inp_f,yarns_elsets,"YARNS")

    box_elsets = inp_f.select_regex(".*BOX.*","elset")
    boxs_elset = CreateElsetFromElsets(inp_f,box_elsets,"BOXS")


    
    if no_shell:
        inp_f.remove_by_type(2)
    else:
        try:
            interface_elsets = inp_f.select_regex(".*INTERFACE.*","elset")
            interface_elset = CreateElsetFromElsets(inp_f,interface_elsets,"INTERFACE")
        except:
            pass

    if "ALMA_Z0_PLANE_NSET" in locals():
        alma_elset = inp_f.select("ALMA","elset")

    carbon_data = carbonfiber()
    resina_data = resina()
    nucleo_data = nucleo()

    Ecarbon_MPa = carbon_data["carbon"].iloc[0]["Young Modulus (GPa)"]*1e3
    poisson_carbon = carbon_data["poisson ratio"]

    materials = {
        "matrix": { "E" : resina_data["young modulus [MPa]"], 
                    "nu": resina_data["poisson ratio"] },
        "carbon": { "E" : Ecarbon_MPa, 
                    "nu": poisson_carbon },
        "nucleo": { "E" : nucleo_data["young modulus [MPa]"],
                    "nu": nucleo_data["poisson ratio"] }
    }

    matrix_material = inp_f.CreateElasticMaterial("matrix",
                                                  materials["matrix"]["E"],
                                                  materials["matrix"]["nu"])
    
    carbon_material = inp_f.CreateElasticMaterial("carbon",
                                                  materials["carbon"]["E"],
                                                  materials["carbon"]["nu"])

    nucleo_material = inp_f.CreateElasticMaterial("nucleo",
                                                    materials["nucleo"]["E"],
                                                    materials["nucleo"]["nu"])

    inp_f.CreateSolidSection(elset_yarns,carbon_material)
    inp_f.CreateSolidSection(boxs_elset,matrix_material)
    
    if "ALMA_Z0_PLANE_NSET" in locals():
        inp_f.CreateSolidSection(alma_elset,nucleo_material)

    if "interface_elset" in locals():
        inp_f.CreateSolidSection(interface_elset,matrix_material)
        #inp_f.CreateShellSection(interface_elset,matrix_material)

    istep = inp_f.CreateStaticStep(nlgeom=False)
    inp_f.CreateElsetAll()
    istep.elsets_print = ["YARNS","ALL","ALMA"]

    ip_Y0 = Y0_PLANE_NSET.id_nodes[0]
    ip_YL = YL_PLANE_NSET.id_nodes[0]

    yL_pos = inp_f.nodes.df["y"][ip_YL]
    y0_pos = inp_f.nodes.df["y"][ip_Y0]
    displ_y = params["epsilon"]*(yL_pos - y0_pos)

    istep.CreateBoundary(Y0_PLANE_NSET,dim=2,displ=0)
    istep.CreateBoundary(YL_PLANE_NSET,dim=2,displ=displ_y)
   
    if "ALMA_Z0_PLANE_NSET" in locals():
        istep.CreateBoundary(ALMA_Z0_PLANE_NSET,dim=3,displ=0.0)

    if params["x_fixed"]:
        istep.CreateBoundary(X0_PLANE_NSET,dim=1,displ=0.0)
        istep.CreateBoundary(XL_PLANE_NSET,dim=1,displ=0.0)



    def element2points(element):
        df_nodes = element.GetNodes(inp_f.nodes)
        df_nodes = pd.concat(df_nodes)
        # remove duplicate nodes
        df_nodes = df_nodes.drop_duplicates()
        return df_nodes
    def element_plane(element):

        df_nodes = element2points(element)

        points = df_nodes[["x","y","z"]].values
        points = [list(point) for point in points]

        return are_coplanar(points)


    elements = [ element 
                for element in inp_f.elements 
                if element.dimension == 2 and element_plane(element)]

    # remove elements
    for element in elements:
        element.name = "DELETE"

    inp_f.cards = [card for card in inp_f.cards if card.name != "DELETE"]
    # array 
    inp_f.cards = np.array(inp_f.cards)


    elements = [ element 
                for element in inp_f.elements 
                if element.dimension == 2 ] 
    
    # remove sufaces
    inp_f.remove_by_type(2)

        
    for element in elements:
        element.options["TYPE"]= "S6"

    # clear previous files
    shutil.rmtree(output_folder, ignore_errors=True)
    # create folder
    os.makedirs(output_folder)

    opt_default = {
        "OMP_NUM_THREADS":4,
        "mpi_np":4,
        "mpi":True
    }
    inp_f.run(output_folder,opt=opt_default)

    return inp_f