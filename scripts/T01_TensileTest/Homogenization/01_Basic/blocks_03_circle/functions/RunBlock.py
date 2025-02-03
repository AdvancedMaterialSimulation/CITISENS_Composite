import gmsh 
from CompositeSandwich.box_labeling import box_labeling
import shutil,os
from djccx.inp.inp import inp
from Composite.inp.CreateNsetFromElset import CreateNsetFromElset
import numpy as np
def RunBlock(params):

    zT = params["zT"]
    volume_fraction = params["volume_fraction"]
    
    epsilon = 0.1 
    Z_displ = epsilon*zT

    Em = params["matrix"]["E"]
    vm = params["matrix"]["nu"]

    Ec = params["carbon"]["E"]
    vc = params["carbon"]["nu"]

    output_folder = params["output_folder"]

    Lx = 2.0
    Ly = 10.0 # lo mas grande posible
    
    radius = np.sqrt(Lx*Ly*volume_fraction/np.pi)



    if radius >= Lx:
        raise ValueError("zmid > Lx")
    
    gmsh.initialize()

    # Un cubo partido en tres partes
    # Para ello haremos primero un cubo y luego un cubo más pequeño en el centro
    # luego con la herramienta de partición de gmsh dividiremos el cubo en tres partes
    # ademas etiquetaremos las tres partes con physical groups como top, middle y bottom



    cube = gmsh.model.occ.addBox(-Lx/2, 0, -zT/2,  # x0, y0, z0
                                  Lx, Ly, +zT)   # dx, dy, dz

    # Cubo más pequeño
    cylinder = gmsh.model.occ.addCylinder(0, 0, 0,  # x0, y0, z0
                                          0, Ly, 0,  # dx, dy, dz
                                            radius)
    
    gmsh.model.occ.synchronize()
    
    #gmsh.fltk.run()
    r = gmsh.model.occ.fragment([(3, cube)], [(3, cylinder)])
    gmsh.model.occ.synchronize()

    mid_tag    = r[0][0][1]
    matrix_tag = r[0][1][1]

    gmsh.model.occ.synchronize()
    # 

    # --------------------------------
    # Etiquetamos las caras
    # --------------------------------
    matrix_ph = gmsh.model.addPhysicalGroup(3, [matrix_tag])
    gmsh.model.setPhysicalName(3, matrix_ph, "MATRIX")

    mid_ph = gmsh.model.addPhysicalGroup(3, [mid_tag])
    gmsh.model.setPhysicalName(3, mid_ph, "MIDDLE")

    # Box labeling 
    box_labeling(matrix_tag,"MATRIX") 

    gmsh.model.occ.synchronize()

    # Mesh
    # setsize
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.4)
    # # curve 
    # gmsh.option.setNumber("Mesh.Algorithm", 6)
    # gmsh.option.setNumber("Mesh.Algorithm3D", 4)
    gmsh.option.setNumber("Mesh.CharacteristicLengthFromCurvature", 10)

    gmsh.model.mesh.generate(3)
    # second order
    gmsh.model.mesh.setOrder(2)
    gmsh.write("cube.inp")
    gmsh.finalize()

    inp_f = inp("cube.inp")

    # --------------------------------
    # Creamos los nsets a partir de los elsets
    # --------------------------------
    bot_surf_elset = inp_f.select("MATRIX_Z0","elset") # Este viene de la función box_labeling
    bot_nset= CreateNsetFromElset(inp_f, bot_surf_elset, "bot")
    
    top_surf_elset = inp_f.select("MATRIX_ZL","elset") # Este viene de la función box_labeling
    top_nset= CreateNsetFromElset(inp_f, top_surf_elset, "top")

    mat_m = inp_f.CreateElasticMaterial("resina", Em, vm)
    mat_c = inp_f.CreateElasticMaterial("carbon", Ec, vc)

    elset_matrix = inp_f.select("MATRIX","elset")
    elset_mid = inp_f.select("MIDDLE","elset")


    # remove 2d elements
    # Solo usamos los elementos 2D para crear los nsets
    # ya no los necesitamos
    inp_f.remove_by_type(2)

    # --------------------------------
    # Section
    # --------------------------------
    inp_f.CreateSolidSection(elset_matrix,mat_m)
    inp_f.CreateSolidSection(elset_mid,mat_c)


    # --------------------------------
    # Step 
    # --------------------------------
    istep = inp_f.CreateStaticStep()
    istep.CreateBoundary(top_nset,3,Z_displ)
    istep.CreateBoundary(bot_nset,3,0.0)

    # remove output folder

    shutil.rmtree(output_folder, ignore_errors=True)
    os.mkdir(output_folder)

    inp_f.run(output_folder)