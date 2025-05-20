
from  .CreateLines.CreateLines import CreateLines
from  .GenerateMeshRVE.GenerateMeshRVE  import GenerateMeshRVE
from  .CreateSimulation.CreateSimulation import CreateSimulation
import os 
from loadsavejson.savejson import savejson
join = os.path.join

printsep = lambda : print("\t"+50*"=")

def RunFullModel(design,root,params):

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
    params["mesh"]["designs_str"] = lines["designs_str"]
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

    output_folder = join(root,"ccx",design)

    print("Input folder: \t", design_folder)
    print("Output folder: \t", output_folder)

    inpf = CreateSimulation(design_folder,
                            output_folder,
                            params["ccx"],
                            no_shell=True)