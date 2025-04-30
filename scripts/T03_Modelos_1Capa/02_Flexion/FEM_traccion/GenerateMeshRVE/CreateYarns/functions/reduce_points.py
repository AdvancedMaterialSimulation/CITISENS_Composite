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
    ts = ts[3:-3]
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

