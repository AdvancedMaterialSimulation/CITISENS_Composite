import gmsh

# load 
def cutgeo(file_1,file_2,file):
    gmsh.initialize()

    # load 
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.Verbosity", 0)

    gmsh.model.add("composite")

    gmsh.model.occ.synchronize()

    gmsh.merge(file_1)
    gmsh.merge(file_2)


    gmsh.model.occ.synchronize()

    # diff
    volume = gmsh.model.getEntities(3)
    hollow_box =  gmsh.model.occ.cut([volume[1]], 
                                    [volume[0]], removeTool=False)

    # synchronize
    gmsh.model.occ.synchronize()
    # mesh
    gmsh.write(file)

    gmsh.fltk.finalize()