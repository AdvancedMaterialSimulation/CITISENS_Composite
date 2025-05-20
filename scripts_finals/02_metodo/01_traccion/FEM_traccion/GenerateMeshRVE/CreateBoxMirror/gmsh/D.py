import gmsh
from .BoxRefine import BoxRefine
def Dgmsh(Lx, Ly, z0, zT):    

    fc_mesh_min = 0.6
    fc_mesh_max = 0.9

    # curvature 

    # create the box field
    field_box_fulllength = BoxRefine(0, Lx, 
                                     0, Ly, 
                                     0, zT/2, 
                                     fc_mesh_max, fc_mesh_max)

    field_box = BoxRefine(0, Lx, 
                          0, Ly, 
                          z0/2, zT/2, fc_mesh_min, fc_mesh_max)
 
    gmsh.option.setNumber("Mesh.Algorithm", 6)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 7)

    border_z_0 = BoxRefine(0, Lx, 
                           0, Ly, 
                           0.9*z0/2, 1.1*z0/2, 
                           0.3*fc_mesh_min, fc_mesh_max,
                           Thickness=0.1)

    border_z_1  = BoxRefine(0, Lx,
                            0, Ly, 
                            0.9*zT/2, 1.1*zT/2, 
                            0.3*fc_mesh_min, fc_mesh_max,
                            Thickness=0.1)
    
    border_y_0 = BoxRefine(0, Lx, 
                           -0.05*Ly, 0.05*Ly, 
                           z0/2,zT/2, 
                           0.2*fc_mesh_min, fc_mesh_max,
                           Thickness=0.1)
    
    border_y_1 = BoxRefine(0, Lx, 
                           0.95*Ly, 1.05*Ly, 
                           z0/2,zT/2, 
                           0.2*fc_mesh_min, fc_mesh_max,
                           Thickness=0.1)
    
    list_fields = [field_box_fulllength, 
                    field_box,
                    border_z_0,
                    border_z_1,
                    border_y_0,
                    border_y_1]

    # min field
    field_min = gmsh.model.mesh.field.add("Min")
    gmsh.model.mesh.field.setNumbers(field_min, "FieldsList", list_fields)

    # set the field to the box
    gmsh.model.mesh.field.setAsBackgroundMesh(field_min)
