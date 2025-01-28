import numpy as np

def are_coplanar(points):
    # Se asume que 'points' es una lista de listas, donde cada lista interna representa las coordenadas de un punto [x, y, z].
    if len(points) < 4:
        # Menos de cuatro puntos siempre son coplanares.
        return True
    
    # Seleccionar el primer punto como referencia.
    reference_point = points[0]
    # Crear vectores desde el punto de referencia hasta los otros puntos.
    vectors = [np.array(point) - np.array(reference_point) for point in points[1:]]
    
    # Crear una matriz a partir de estos vectores.
    matrix = np.stack(vectors).T
    
    # Calcular el rango de la matriz.
    rank = np.linalg.matrix_rank(matrix,tol=1e-3)
    
    # Si el rango es menor o igual a 2, los puntos son coplanares.
    return rank <= 2