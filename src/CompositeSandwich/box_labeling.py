
import gmsh
import numpy as np

def box_labeling(tag, label):
    """
    Etiqueta las superficies de un volumen 3D en un modelo de GMSH basado en sus posiciones 
    relativas a los límites en las direcciones `x`, `y` y `z`.

    Args:
        tag (int): Identificador del volumen 3D en el modelo GMSH.
        label (str): Prefijo para las etiquetas de los grupos físicos.

    Returns:
        dict: Un diccionario donde las claves son nombres simplificados de las superficies
              (por ejemplo, "x0", "yL") y los valores son listas de identificadores de superficies 
              asociadas a cada límite.

    Description:
        La función realiza las siguientes tareas:
        1. Obtiene las superficies que delimitan el volumen especificado mediante `getBoundary`.
        2. Calcula los centros de masa de las superficies para determinar sus posiciones.
        3. Identifica los límites del volumen en cada dirección (`x`, `y`, `z`) utilizando los 
           valores mínimo (`0`) y máximo (`L`) de las coordenadas.
        4. Clasifica las superficies según su proximidad a los límites definidos.
        5. Crea grupos físicos en GMSH para cada conjunto de superficies en los límites y les 
           asigna nombres basados en el prefijo `label` y la dirección/límite correspondiente.
        6. Devuelve un diccionario que asocia las etiquetas de los límites con los identificadores 
           de las superficies incluidas en cada grupo físico.

    Example:
        ```python
        import gmsh

        gmsh.initialize()
        gmsh.model.add("example")
        
        # Crear un cubo como ejemplo
        cube = gmsh.model.occ.addBox(0, 0, 0, 1, 1, 1)
        gmsh.model.occ.synchronize()

        # Etiquetar las superficies del cubo
        labels = box_labeling(cube, "myCube")
        
        # Resultado: {"x0": [...], "xL": [...], "y0": [...], "yL": [...], "z0": [...], "zL": [...]}
        print(labels)
        
        gmsh.finalize()
        ```
    """
    
    volumen = gmsh.model.getBoundary([(3,tag)], oriented=False)

    surfaces = []
    for surface in volumen:
        surfaces.append({
            "surface" : surface[1],
            "pos" : gmsh.model.occ.getCenterOfMass(2,surface[1])
        })

    positions = [i["pos"] for i in surfaces]
    positions = np.array(positions)

    xlims = [np.min(positions[:,0]), np.max(positions[:,0])]
    ylims = [np.min(positions[:,1]), np.max(positions[:,1])]
    zlims = [np.min(positions[:,2]), np.max(positions[:,2])]

    surfaces_x0 = [ i for i in surfaces if np.abs(i["pos"][0] - xlims[0]) < 1e-4 ]
    surfaces_xL = [ i for i in surfaces if np.abs(i["pos"][0] - xlims[1]) < 1e-4 ]

    surfaces_y0 = [ i for i in surfaces if np.abs(i["pos"][1] - ylims[0]) < 1e-4 ]
    surfaces_yL = [ i for i in surfaces if np.abs(i["pos"][1] - ylims[1]) < 1e-4 ]

    surfaces_z0 = [ i for i in surfaces if np.abs(i["pos"][2] - zlims[0]) < 1e-4 ]
    surfaces_zL = [ i for i in surfaces if np.abs(i["pos"][2] - zlims[1]) < 1e-4 ]

    directions = ['x', 'y', 'z']
    limits = [xlims, ylims, zlims]
    surfaces_limits = [surfaces_x0, surfaces_xL, 
                       surfaces_y0, surfaces_yL, 
                       surfaces_z0, surfaces_zL]
    ph_list = {}
    for i, direction in enumerate(directions):
        for j, limit in enumerate(['0', 'L']):
            surfaces = surfaces_limits[2*i + j]
            name = f"{label}_{direction}{limit}"
            name_nolabel = f"{direction}{limit}"
            surf_obj = [s["surface"] for s in surfaces]
            ph = gmsh.model.addPhysicalGroup(2, surf_obj, -1)
            gmsh.model.setPhysicalName(2, ph, name)
            ph_list[name_nolabel] = surf_obj


    return ph_list

