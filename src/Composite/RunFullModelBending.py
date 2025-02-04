
from  .CreateLines.CreateLines import CreateLines
from  .GenerateMeshRVE import GenerateMeshRVE
from  .CreateSimulation.CreateSimulation import CreateSimulation
import os 
from loadsavejson.savejson import savejson
join = os.path.join

def RunFullModelBending(design,root,params):

    lines = {
        "r": 2.5,
        "Nx_sq": 2,
        "Ny_sq": 3,
        "type":  'sin' # 'circle' or 'sin'
    }
    lines = CreateLines(lines)

    params["longs"] = lines["longs"]
    

    ouput_folder_designs = join(root,"designs")

    design_folder = join(ouput_folder_designs,design)
    output_folder = join(root,"ccx",design)


    print("\t"+50*"=")
    print("\t"+"Design %s" % design)
    print("\t"+50*"=")

    GenerateMeshRVE(lines,
                    design,
                    ouput_folder_designs,
                    params["mesh"])
    savejson(params,join(root,"params.json"))

    print("\t"+50*"=")
    print("\t"+"CCX %s" % design)
    print("\t"+50*"=")
    print("Input folder: \t", design_folder)
    print("Output folder: \t", output_folder)
    inpf = CreateSimulation(design_folder,
                            output_folder,
                            params["ccx"],
                            no_shell=True)