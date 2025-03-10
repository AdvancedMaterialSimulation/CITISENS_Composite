def get_vector(list_of_layers):
    """
    Genera un vector binario de 4 dimensiones basado en la presencia de ciertas capas en la lista de entrada.

    Args:
        list_of_layers (list): Lista de capas que pueden incluir "X", "SX", "Y" y "SY".

    Returns:
        list: Un vector de 4 elementos donde:
            - La primera posición es 1 si "X" está en list_of_layers, de lo contrario es 0.
            - La segunda posición es 1 si "SX" está en list_of_layers, de lo contrario es 0.
            - La tercera posición es 1 si "Y" está en list_of_layers, de lo contrario es 0.
            - La cuarta posición es 1 si "SY" está en list_of_layers, de lo contrario es 0.
    """
    
    vector = [0, 0, 0, 0]  # Inicializa el vector con ceros
    

    # es mejor contar cuántas veces aparece cada capa en la lista y asignar el valor correspondiente
    vector[0] = list_of_layers.count("X")
    vector[1] = list_of_layers.count("SX")
    vector[2] = list_of_layers.count("Y")
    vector[3] = list_of_layers.count("SY")


    return vector
