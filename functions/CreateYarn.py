import gmsh
import numpy as np
def reduce_points(trajs, num_points=80,d0 = None):
    """
    Reduce el número de puntos de una trayectoria interpolando uniformemente.
    
    Args:
        trajs (np.ndarray): Trayectoria original de forma (N, 3).
        num_points (int): Número deseado de puntos en la nueva trayectoria.
    
    Returns:
        np.ndarray: Trayectoria reducida con forma (num_points, 3).
    """
    # Calcular diferencias y longitudes acumuladas
    diff = np.diff(trajs, axis=0)
    segment_lengths = np.linalg.norm(diff, axis=1)
    cum_lengths = np.concatenate([[0], np.cumsum(segment_lengths)])  # Longitud acumulada
    
    # Crear una nueva distribución de puntos equidistantes
    ts = np.linspace(0, cum_lengths[-1], num_points)

    # d0 must be the first distance and the last distance
    if d0 is not None:
        ts = ts[ ts >= d0 ]
        ts = ts[ ts <= cum_lengths[-1] - d0 ]

        ts = np.concatenate(([0], 
                             [d0], 
                             ts, 
                             [cum_lengths[-1]-d0], 
                             [cum_lengths[-1]]))

    
    # Interpolar para obtener los nuevos puntos
    x = np.interp(ts, cum_lengths, trajs[:, 0])
    y = np.interp(ts, cum_lengths, trajs[:, 1])
    z = np.interp(ts, cum_lengths, trajs[:, 2])
    
    # Combinar las coordenadas en una nueva trayectoria
    reduced_trajs = np.column_stack((x, y, z))

    # last points 
    last_point = reduced_trajs[-1].copy()

    last_point = last_point + np.array([4,0,0])

    
    reduced_trajs = np.concatenate((reduced_trajs, last_point.reshape(1,3)), axis=0)
    
    return reduced_trajs


# =============================================================================

def CreateYarn(params):

    printw = lambda *args: print("[CreateYarn]", *args)

    trajs  = params["trajs"]
    file   = params["file"]
    radius = params["radius"]
    num_points = params["num_points"]

    angle_init = np.arctan2(trajs[1][1] - trajs[0][1], trajs[1][0] - trajs[0][0])
    angle_end = np.arctan2(trajs[-1][1] - trajs[-2][1], trajs[-1][0] - trajs[-2][0])

    angle = (angle_init + angle_end)/2


    printw("angle", angle * 180/np.pi, "º")
    printw("radius", radius)
    printw("radius/np.cos(angle)", radius/np.cos(angle))
    
    rstart = radius/np.cos(angle)
    d0 = np.sqrt(rstart**2 - radius**2) + 0.25*radius

    # if d0 < radius then d0 = radius
    if d0 < radius/2:
        d0 = radius/2

    printw("d0", d0)

    trajs = reduce_points(trajs, num_points=num_points,d0=d0)

    trajs_vec = np.diff(trajs, axis=0)
    # 
    # # 1 vec is 
    trajs_vec[0] =[1,0,0] 
    trajs_vec[-1] = [1,0,0]

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

    # add ellipse r' = r/cos(angle)
    x, y, z = trajs[0]
    disk = gmsh.model.occ.addEllipse(x, y, z, 
                                     r/np.cos(angle),
                                     r, id,
                                     zAxis=trajs_vec[0],
                                     xAxis=[0,1,0])
    id += 1
    disks.append(disk)
    wires.append(gmsh.model.occ.addWire([disk]))

    for i in range(1,len(trajs)-2):
        x, y, z = trajs[i]
        disk = gmsh.model.occ.addCircle(x, y, z, r, id,
                                        zAxis=trajs_vec[i],
                                        xAxis=[0,1,0])
        # crear loop from disk
        
        disks.append(disk)
        wires.append(gmsh.model.occ.addWire([disk]))
        id += 1

    # last angle
    x, y, z = trajs[-2]
    disk = gmsh.model.occ.addEllipse(x, y, z, 
                                     r/np.cos(angle), r, 
                                     id,
                                     zAxis=trajs_vec[-1],
                                     xAxis=[0,1,0])
    disks.append(disk)
    wires.append(gmsh.model.occ.addWire([disk]))

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

    try:
        gmsh.fltk.run()
    except:
        pass
    
   # save geometry
    gmsh.write(file) 
    # Finalizar GMSH
    gmsh.finalize()