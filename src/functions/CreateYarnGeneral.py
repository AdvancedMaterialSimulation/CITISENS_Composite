import gmsh
import numpy as np
def reduce_points(trajs, num_points=80,density=None):
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
    diff = np.diff(trajs, axis=0)
    segment_lengths = np.linalg.norm(diff, axis=1)
    cum_lengths = np.concatenate([[0], np.cumsum(segment_lengths)])  # Longitud acumulada
    
    # Crear una nueva distribución de puntos equidistantes
    ts = np.linspace(0, cum_lengths[-1], num_points)
    
    # Interpolar para obtener los nuevos puntos
    x = np.interp(ts, cum_lengths, trajs[:, 0])
    y = np.interp(ts, cum_lengths, trajs[:, 1])
    z = np.interp(ts, cum_lengths, trajs[:, 2])
    
    # Combinar las coordenadas en una nueva trayectoria
    reduced_trajs = np.column_stack((x, y, z))

    # last points     
    return reduced_trajs


# =============================================================================

def CreateYarn(params):

    plausible_final =np.array([[1,0,0], [0,1,0], [-1,0,0], [0,-1,0] ] )

    printw = lambda *args: print("[CreateYarn]", *args)

    trajs  = params["trajs"]
    file   = params["file"]
    radius = params["radius"]
    density = params["density"] 
    trajs = reduce_points(trajs, density=density)

    trajs_vec = np.diff(trajs, axis=0)

    distance_to_plausible = lambda x: np.linalg.norm(x - plausible_final, axis=1)

    # get the plausible vector
    last_vector = trajs_vec[-1]
    last_vector = last_vector / np.linalg.norm(last_vector)
    last_vector = plausible_final[np.argmin(distance_to_plausible(last_vector))].copy()

    trajs_vec = np.concatenate((trajs_vec, [last_vector]), axis=0)


    # first vector
    first_vector = trajs_vec[0]
    first_vector = first_vector / np.linalg.norm(first_vector)
    first_vector = plausible_final[np.argmin(distance_to_plausible(first_vector))].copy()
    trajs_vec[0] = first_vector
    # 

    # Iniciar GMSH
    gmsh.initialize()
    gmsh.option.setNumber("Geometry.Tolerance", 1e-5)  # Ajusta la tolerancia
    #verbose of 
    gmsh.option.setNumber("General.Terminal", 0)

    gmsh.model.add("Fourier_Cylinder_OCC_Pipe")

    # Parámetros de la trayectoria
    # given x,y,z, r
    # add disk 

    id = 0
    r = radius
    disks = []
    wires = []

    # first angle 


    for i in range(len(trajs)):
        x, y, z = trajs[i]
        disk = gmsh.model.occ.addCircle(x, y, z, r, id,
                                        zAxis=trajs_vec[i],
                                        xAxis=[0,0,1])
        # crear loop from disk
        
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