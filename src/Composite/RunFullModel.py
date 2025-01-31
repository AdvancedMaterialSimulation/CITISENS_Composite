
from Composite.CreateLines.CreateLines import CreateLines
from Composite.GenerateMeshRVE import GenerateMeshRVE
from Composite.CreateSimulation.CreateSimulation import CreateSimulation
import os 

join = os.path.join
def RunFullModel(design,root,params):

    lines = {
        "r": 2.5,
        "Nx_sq": 1,
        "Ny_sq": 1,
        "type":  'sin' # 'circle' or 'sin'
    }

    lines = CreateLines(lines)

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

    print("\t"+50*"=")
    print("\t"+"CCX %s" % design)
    print("\t"+50*"=")
    print("Input folder: \t", design_folder)
    print("Output folder: \t", output_folder)
    inpf = CreateSimulation(design_folder,
                            output_folder,
                            params["ccx"],
                            no_shell=True)