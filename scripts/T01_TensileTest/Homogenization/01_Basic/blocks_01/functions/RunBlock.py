import gmsh 
from CompositeSandwich.box_labeling import box_labeling
import shutil,os
from djccx.inp.inp import inp
from Composite.inp.CreateNsetFromElset import CreateNsetFromElset

def RunBlock(params):

    zT = params["zT"]
    zmid_factor = params["zmid_factor"]
    zmid = zT*zmid_factor

    epsilon = 0.1 
    Z_displ = epsilon*zT

    Em = params["matrix"]["E"]
    vm = params["matrix"]["nu"]

    Ec = params["carbon"]["E"]
    vc = params["carbon"]["nu"]

    output_folder = params["output_folder"]

    gmsh.initialize()

    # Un cubo partido en tres partes
    # Para ello haremos primero un cubo y luego un cubo más pequeño en el centro
    # luego con la herramienta de partición de gmsh dividiremos el cubo en tres partes
    # ademas etiquetaremos las tres partes con physical groups como top, middle y bottom

    Lx = 1.0
    Ly = 10.0

    cube = gmsh.model.occ.addBox(0, 0, -zT/2,  # x0, y0, z0
                                 Lx, Ly, +zT)   # dx, dy, dz

    # Cubo más pequeño
    small_cube = gmsh.model.occ.addBox(0.0, 0.0, -zmid/2,  # x0, y0, z0
                                       Lx, Ly,  zmid)   # dx, dy, dz

    # Partición

    gmsh.model.occ.synchronize()


    r = gmsh.model.occ.cut([(3, cube)], [(3, small_cube)], removeTool=False)
    gmsh.model.occ.synchronize()

    # Etiquetado
    # Definimos los grupos físicos

    middle = gmsh.model.addPhysicalGroup(3, [small_cube])
    gmsh.model.setPhysicalName(3, middle, "middle")

    top_tag = r[0][1][1]
    bot_tag = r[0][0][1]

    top_ph = gmsh.model.addPhysicalGroup(3, [top_tag])
    gmsh.model.setPhysicalName(3, top_ph, "top")

    bot_ph = gmsh.model.addPhysicalGroup(3, [bot_tag])
    gmsh.model.setPhysicalName(3, bot_ph, "bot")

    # Box labeling 
    box_labeling(bot_tag,"bot") 
    box_labeling(top_tag,"top")

    gmsh.model.occ.synchronize()

    # Mesh
    # setsize
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 0.4)


    gmsh.model.mesh.generate(3)
    # second order
    gmsh.model.mesh.setOrder(2)
    gmsh.write("cube.inp")
    gmsh.finalize()

    inp_f = inp("cube.inp")

    # --------------------------------
    # Creamos los nsets a partir de los elsets
    # --------------------------------
    bot_surf_elset = inp_f.select("BOT_Z0","elset") # Este viene de la función box_labeling
    bot_nset= CreateNsetFromElset(inp_f, bot_surf_elset, "bot")
    
    top_surf_elset = inp_f.select("TOP_ZL","elset") # Este viene de la función box_labeling
    top_nset= CreateNsetFromElset(inp_f, top_surf_elset, "top")

    mat_m = inp_f.CreateElasticMaterial("MAT_1", Em, vm)
    mat_c = inp_f.CreateElasticMaterial("MAT_2", Ec, vc)

    elset_bot = inp_f.select("BOT","elset")
    elset_top = inp_f.select("TOP","elset")
    elset_mid = inp_f.select("MIDDLE","elset")

    # remove 2d elements
    # Solo usamos los elementos 2D para crear los nsets
    # ya no los necesitamos
    inp_f.remove_by_type(2)

    # --------------------------------
    # Section
    # --------------------------------
    inp_f.CreateSolidSection(elset_bot,mat_m)
    inp_f.CreateSolidSection(elset_top,mat_m)

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