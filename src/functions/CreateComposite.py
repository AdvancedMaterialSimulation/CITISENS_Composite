# load fourier_cylinder_occ_pipe.stl

import gmsh
import numpy as np

def CreateComposite(params):

    file = params["file"]
    yarn_file = params["yarn_file"]
    radius = params["radius"]
    trajs = params["trajs"]
    h = params["h"]
    Ny = params["Ny"]
    
    
    # Ny must be integer
    assert Ny == int(Ny), "Ny must be integer"
    #h must be float and positive
    assert h > 0, "h must be positive"
    
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    gmsh.model.add("fourier_cylinder_occ_pipe")

    gmsh.option.setNumber("General.Terminal", 0)



    x0 = np.min(trajs[:,0])

    dy = np.max(trajs[:,1])  - np.min(trajs[:,1])
    dx = np.max(trajs[:,0])  - x0

    gmsh.open(yarn_file)

    volume_yarn = gmsh.model.getEntities(3)[-1]


    gmsh.model.occ.synchronize()

    # repetitions 
    for i in range(1,Ny):
        yarn_copy = gmsh.model.occ.copy([volume_yarn])
        gmsh.model.occ.translate(yarn_copy
                                , 0, h*i, 0)
        gmsh.model.occ.synchronize()

    Lx = dx
    y0 = - dy/2 - 2*radius
    Ly = (Ny-1)*h - 2*y0 + radius
    Lz = 3*radius 
    z0 = -Lz/2

    
    yarns = gmsh.model.getEntities(3)

    box = gmsh.model.occ.addBox(x0, y0, z0, Lx, Ly, Lz)

    # cut 
    gmsh.model.occ.cut([(3, box)], yarns, removeTool=False)

    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", radius*0.1)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 4*radius)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 10)
    gmsh.option.setNumber("Mesh.AngleSmoothNormals", 10)
    gmsh.option.setNumber("Mesh.Smoothing", 10)	
    gmsh.option.setNumber("Mesh.Algorithm", 2)


    # gmsh.option.setNumber("Mesh.AngleToleranceFacetOverlap", 0.1)
    # 

    # use points trajs to create a refined mesh

    # take 10 points from trajs
    

    try:
        gmsh.fltk.run()
    except:
        pass
    
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.setOrder(2)


    gmsh.write(file)
    gmsh.finalize()