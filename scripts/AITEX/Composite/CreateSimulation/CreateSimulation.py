from djccx.inp.inp import inp
from Composite.inp.CreateNsetFromElset import CreateNsetFromElset
from Composite.inp.CreateElsetFromElsets import CreateElsetFromElsets
from validation.experimental import carbonfiber,resina
import os
def CreateSimulation(composite,no_shell=True):

    inp_f = inp(os.path.join(composite,
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
    ALMA_Z0_PLANE = inp_f.select("ALMA_Z0","elset")

    PLUS_ZL_PLANE_NSET = CreateNsetFromElset(inp_f,PLUS_ZL_PLANE,name="PLUS_ZL_PLANE")
    ALMA_Z0_PLANE_NSET = CreateNsetFromElset(inp_f,ALMA_Z0_PLANE,name="ALMA_Z0_PLANE")

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

    alma_elset = inp_f.select("ALMA","elset")

    carbon_data = carbonfiber()
    resina_data = resina()

    Ecarbon_MPa = carbon_data["carbon"].iloc[0]["Young Modulus (GPa)"]*1e3
    poisson_carbon = carbon_data["poisson ratio"]

    materials = {
        "matrix": { "E" : resina_data["young modulus [MPa]"], 
                    "nu": resina_data["poisson ratio"] },
        "carbon": { "E" : Ecarbon_MPa, 
                    "nu": poisson_carbon }
    }

    matrix_material = inp_f.CreateElasticMaterial("matrix",
                                                  materials["matrix"]["E"],
                                                  materials["matrix"]["nu"])
    
    carbon_material = inp_f.CreateElasticMaterial("carbon",
                                                  materials["carbon"]["E"],
                                                  materials["carbon"]["nu"])


    inp_f.CreateSolidSection(elset_yarns,carbon_material)
    inp_f.CreateSolidSection(boxs_elset,matrix_material)
    inp_f.CreateSolidSection(alma_elset,matrix_material)

    if "interface_elset" in locals():
        inp_f.CreateSolidSection(interface_elset,matrix_material)
        #inp_f.CreateShellSection(interface_elset,matrix_material)

    istep = inp_f.CreateStaticStep(nlgeom=False)

    istep.CreateBoundary(Y0_PLANE_NSET,dim=2,displ=0)
    istep.CreateBoundary(YL_PLANE_NSET,dim=2,displ=0.2)


    istep.CreateBoundary(ALMA_Z0_PLANE_NSET,dim=3,displ=0.0)

    return inp_f
    output_folder = "output/ccx"

    opt= {
    "OMP_NUM_THREADS":4,
    "mpi_np":6,
    "mpi":True
}
    inp_f.run(output_folder,opt=opt)

    return inp_f