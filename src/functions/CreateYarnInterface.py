import gmsh
import numpy as np

def nearest_multiple_of_six(n):
    # Encuentra el múltiplo de 6 más cercano hacia abajo
    lower = n - (n % 6)
    # Encuentra el múltiplo de 6 más cercano hacia arriba
    upper = lower if n % 6 == 0 else lower + 6
    
    # Determina cuál múltiplo está más cerca del número original
    if (n - lower) <= (upper - n):
        return lower
    else:
        return upper
    
def reduce_points(trajs,radius, num_points=80,density=None):
    """
    Reduce el número de puntos de una trayectoria interpolando uniformemente.
    
    Args:
        trajs (np.ndarray): Trayectoria original de forma (N, 3).
        num_points (int): Número deseado de puntos en la nueva trayectoria.
    
    Returns:
        np.ndarray: Trayectoria reducida con forma (num_points, 3).
    """
    # Calcular diferencias y longitudes acumuladas
    if density is not None:
        long = np.linalg.norm(np.diff(trajs, axis=0), axis=1)
        long  = np.sum(long)
        num_points = int(long*density)
        # debera ser multiplo de 6 + 4 
        #num_points = nearest_multiple_of_six(num_points) + 2 + 1
    diff = np.diff(trajs, axis=0)
    segment_lengths = np.linalg.norm(diff, axis=1)
    cum_lengths = np.concatenate([[0], np.cumsum(segment_lengths)])  # Longitud acumulada
    
    # Crear una nueva distribución de puntos equidistantes
    ts = np.linspace(0, cum_lengths[-1], num_points)
    # remove
    ts = ts[2:-2]
    # add again the first and last point
    ts = np.concatenate([[0], ts, [cum_lengths[-1]]])
    
    # Interpolar para obtener los nuevos puntos
    x = np.interp(ts, cum_lengths, trajs[:, 0])
    y = np.interp(ts, cum_lengths, trajs[:, 1])
    z = np.interp(ts, cum_lengths, trajs[:, 2])
    
    # Combinar las coordenadas en una nueva trayectoria
    reduced_trajs = np.column_stack((x, y, z))

    ts_fine = np.linspace(0, cum_lengths[-1], 10*num_points)
    x_fine = np.interp(ts_fine, cum_lengths, trajs[:, 0])
    y_fine = np.interp(ts_fine, cum_lengths, trajs[:, 1])
    z_fine = np.interp(ts_fine, cum_lengths, trajs[:, 2])

    trajs_fine = np.column_stack((x_fine, y_fine, z_fine))

    trac_vec = np.diff(trajs_fine, axis=0)
    # last vector must be the same as the last vector in the original trajectory
    # 
    trac_vec = np.concatenate((trac_vec, [trac_vec[-1].copy()]), axis=0)

    # traj_vec must have the same length as the original trajectory
    trac_vec_x = np.interp(ts, ts_fine, trac_vec[:, 0])
    trac_vec_y = np.interp(ts, ts_fine, trac_vec[:, 1])
    trac_vec_z = np.interp(ts, ts_fine, trac_vec[:, 2])

    trac_vec = np.column_stack((trac_vec_x, trac_vec_y, trac_vec_z))
    # last points     
    #print(len(reduced_trajs))
    return reduced_trajs, trac_vec


# =============================================================================

def CreateYarn(params):

    plausible_final =np.array([[1,0,0], [0,1,0], [-1,0,0], [0,-1,0] ] )

    printw = lambda *args: print("[CreateYarn]", *args)

    trajs  = params["trajs"]
    file   = params["file"]
    radius = params["radius"]
    density = params["density"] 
    trajs,trajs_vec = reduce_points(trajs, radius,density=density)

    first_vector_computed = trajs_vec[0].copy()
    first_vector_computed = first_vector_computed / np.linalg.norm(first_vector_computed)
    last_vector_computed  = trajs_vec[-1].copy()
    last_vector_computed = last_vector_computed / np.linalg.norm(last_vector_computed)

    distance_to_plausible = lambda x: np.linalg.norm(x - plausible_final, axis=1)

    # get the plausible vector
    last_vector = trajs_vec[-1]
    last_vector = last_vector / np.linalg.norm(last_vector)
    last_vector = plausible_final[np.argmin(distance_to_plausible(last_vector))].copy()

    trajs_vec[-1] = last_vector


    # first vector
    first_vector = trajs_vec[0]
    first_vector = first_vector / np.linalg.norm(first_vector)
    first_vector = plausible_final[np.argmin(distance_to_plausible(first_vector))].copy()
    trajs_vec[0] = first_vector
    # 
    # angle 
    angle_first = np.arccos(np.dot(first_vector_computed, first_vector))
    angle_last = np.arccos(np.dot(last_vector_computed, last_vector))
    # Iniciar GMSH
    gmsh.initialize()
    gmsh.clear()

    gmsh.option.setNumber("Geometry.Tolerance", 1e-5)  # Ajusta la tolerancia
    #verbose of 
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.Verbosity", 0)


    gmsh.model.add("Fourier_Cylinder_OCC_Pipe")

    # Parámetros de la trayectoria
    # given x,y,z, r
    # add disk 

    id = 0
    r = radius
    disks = []
    wires = []

    # first angle 


    # first disk can be a ellipse 
    x, y, z = trajs[0]
    r2 = r

    r1 = r / np.cos(angle_first)
    xAxis = np.cross(trajs_vec[0], [0,0,1])
    disk = gmsh.model.occ.addEllipse(x, y, z, 
                                      r1, r2, id, 
                                      zAxis=trajs_vec[0], 
                                      xAxis=xAxis)
    disks.append(disk)
    wires.append(gmsh.model.occ.addWire([disk]))
    id += 1
    
    for i in range(1,len(trajs)-1):
        x, y, z = trajs[i]

        # xAxis is trajs_vec[i] and  z = [0,0,1]
        xAxis = np.cross(trajs_vec[i], [0,0,1])

        disk = gmsh.model.occ.addCircle(x, y, z, r, id,
                                        zAxis=trajs_vec[i],
                                        xAxis=xAxis)
        # crear loop from disk
        
        disks.append(disk)
        wires.append(gmsh.model.occ.addWire([disk]))
        id += 1

    # last disk
    x, y, z = trajs[-1]
    r2 = r
    r1 = r / np.cos(angle_last)
    xAxis = np.cross(trajs_vec[-1], [0,0,1])
    disk = gmsh.model.occ.addEllipse(x, y, z, 
                        r1, r2, id, 
                        zAxis=trajs_vec[-1], 
                        xAxis=xAxis)
    disks.append(disk)
    wires.append(gmsh.model.occ.addWire([disk]))
    id += 1

    gmsh.model.occ.synchronize()
    # addThruSections
    volumes = []
    for i in range(len(disks)-1):
        v = gmsh.model.occ.addThruSections([wires[i], wires[i+1]],
                                           makeSolid=True)
        volumes.append(v)


    for i in range(10000):
        volumes = gmsh.model.occ.getEntities(3)
        try:
            gmsh.model.occ.fuse([volumes[-1]],
                                [volumes[-2]],
                                removeObject=True,
                                removeTool=True)
        except:
            break
        gmsh.model.occ.synchronize()

    # save geometry

    gmsh.model.occ.synchronize()

    # try:
    #     gmsh.fltk.run()
    # except:
    #     pass
    
   # save geometry
    gmsh.write(file) 
    # Finalizar GMSH
    gmsh.finalize()