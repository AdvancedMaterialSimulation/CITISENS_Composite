from djccx.inp.inp import inp
import os,shutil
from .CreateComposite.CreateComposite import CreateComposite


fc_mesh_max_d = {
    "A": 1.0,
    "Adouble": 1.0,
    "B": 1.0,
    "B1":2.0,
    "C": 1.0,
    "D": 1.0,
    "E": 1.0, # 2.5
    "F": 1.0,
    "SX": 1.0,
    "SY": 1.0,
    "SX_smooth": 2.0,
    "SY_smooth": 2.0,
    "X": 1.0,
    "Y": 1.0,
}
fm_max_default = 2.5
fc_mesh_min_d = {
    "A": 0.2,
    "Adouble": 0.25,
    "B": 0.2,
    "B1":0.5,
    "C": 0.25,
    "D": 0.25,
    "E": 0.25, # 0.45
    "F": 0.25,
    "SX": 0.2,
    "SY": 0.2,
    "SX_smooth": 0.5,
    "SY_smooth": 0.5,
    "X": 0.2,
    "Y": 0.2,
}
fm_min_default = 0.5


# ==============================================================================

# fc_mesh_max_d = {
#     "A": 2.0,
#     "Adouble": 1.5,
#     "B": 1.0,
#     "B1":2.0,
#     "C": 1.0,
#     "D": 1.0,
#     "E": 1.0, # 2.5
#     "F": 1.0,
#     "SX": 1.0,
#     "SY": 1.0,
#     "SX_smooth": 2.0,
#     "SY_smooth": 2.0,
#     "X": 1.0,
#     "Y": 1.0,
# }
# fm_max_default = 2.5
# fc_mesh_min_d = {
#     "A": 0.2,
#     "Adouble": 0.35,
#     "B": 0.2,
#     "B1":0.5,
#     "C": 0.25,
#     "D": 0.25,
#     "E": 0.25, # 0.45
#     "F": 0.25,
#     "SX": 0.2,
#     "SY": 0.2,
#     "SX_smooth": 0.5,
#     "SY_smooth": 0.5,
#     "X": 0.2,
#     "Y": 0.2,
# }

def GenerateMeshRVE(lines,select_design,output_folder,params_composite):

    output_folder = os.path.join(output_folder,select_design)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    params_composite["trajs_layers"] = lines["designs"][select_design]
    
    params_composite["fc_mesh_min"] = fc_mesh_min_d[select_design]
    params_composite["fc_mesh_max"] = fc_mesh_max_d[select_design]

    params_composite["Lx"] = lines["Lx"]
    params_composite["Ly"] = lines["Ly"]


    output_folder = output_folder.split(os.sep)
    params_composite = CreateComposite(params_composite,output_folder)

    if not params_composite["check_jacobian"]:
        return True
    
    inp_f = inp(os.path.join(*output_folder,"composite.inp"))
    inp_f.remove_by_type(1)
    inp_f.remove_by_type(2)

    elset_all = inp_f.CreateElsetAll()
    material  = inp_f.CreateElasticMaterial(name="Material-1",E=1e6,nu=0.3)
    section   = inp_f.CreateSolidSection(elset=elset_all,material=material)

    istep = inp_f.CreateStaticStep(nlgeom=False)

    # create ccx insid
    os.makedirs(os.path.join(*output_folder,"ccx"))

    inp_f.print(file=os.path.join(*output_folder,"ccx","test.inp"))

    try:
        opt_default = {"OMP_NUM_THREADS":4,
                            "mpi_np":4,
                            "mpi":True}
        
        run_folder = os.path.join(*output_folder,"ccx")
        inp_f.run(run_folder,opt=opt_default)
        work = True
    except:
        print("Error in the inp file")
        work = False

    print(50*"-")
    print("Done")
    print(50*"-")

    return work