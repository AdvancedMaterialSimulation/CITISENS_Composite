
from  .CreateLines.CreateLines import CreateLines
from  .GenerateMeshRVE.GenerateMeshRVE  import GenerateMeshRVE
from  .CreateSimulation.CreateSimulation import CreateSimulation
import os 
from loadsavejson.savejson import savejson
join = os.path.join

printsep = lambda : print("\t"+50*"=")

def RunFullModel(design,root,params,E_pairs):

    # ==========================================================
    # 1. Create the lines
    # ==========================================================
    lines = {
        "r": 2.5,
        "Nx_sq": 1,
        "Ny_sq": 1,
        "type":  'sin' # 'circle' or 'sin'
    }
    lines = CreateLines(lines)

    params["longs"] = lines["longs"]

    if not os.path.exists(root):
        os.makedirs(root)
        
    savejson(params,join(root,"params.json"))


    # ==========================================================
    # 2. Generate the mesh
    # ==========================================================
    ouput_folder_designs = join(root,"designs")

    design_folder = join(ouput_folder_designs,design)

    printsep()
    print("\t"+"Design %s" % design)
    printsep()

    GenerateMeshRVE(lines,
                    design,
                    ouput_folder_designs,
                    params["mesh"])

    # ==========================================================
    # 3. Create the simulation (inp file) and run it
    # ==========================================================


    printsep()
    print("\t"+"CCX %s" % design)
    printsep()

    for j,E_pair in enumerate(E_pairs):
 
        params_copy = params.copy()
        params_copy["ccx"]["E_carbon"] = E_pair[1]
        params_copy["ccx"]["E_resina"] = E_pair[0]
    
        output_folder = join(root,"ccx",design,"E_",str(j).zfill(2))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        print("Input folder: \t", design_folder)
        print("Output folder: \t", output_folder)

        inpf = CreateSimulation(design_folder,
                                output_folder,
                                params_copy["ccx"],
                                no_shell=True)