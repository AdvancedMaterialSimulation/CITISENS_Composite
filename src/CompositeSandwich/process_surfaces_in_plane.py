import numpy as np
import gmsh

def process_surfaces_in_plane(surfaces, coord, value, layer_name, plane,name):
    """
    Procesa las superficies en un plano específico y las clasifica en circulares y rectangulares.
    Crea grupos físicos y nombres para estas superficies.

    :param surfaces: Lista de superficies
    :param coord: Índice de la coordenada (0 para x, 1 para y) nunca se usa 2 porque es z
    :param value: Valor del plano (0, Lx, Ly, etc.)
    :param layer_name: Nombre base de la capa
    :param plane: Identificador del plano ("x", "y", etc.)
    :param name: Nombre de la capa ("0", "L", etc.)
    """
    positions = [surface[1][coord] for surface in surfaces]
    surfaces_in_plane = [surface for i, surface in enumerate(surfaces) if np.abs(positions[i] - value) < 1e-6]
    surfaces_in_plane = sorted(surfaces_in_plane, key=lambda x: x[1][1 - coord])

    len_s_in_plane = [len(gmsh.model.getBoundary([surface[0]], oriented=False, recursive=False))
                      for surface in surfaces_in_plane]
    
    # Separar en círculos y rectángulos

    def is_circle(lens):
        if lens == 1 or lens == 3:
            return True
        else:
            return False

    circles = [surface for i, surface in enumerate(surfaces_in_plane) if is_circle(len_s_in_plane[i])]
    rectangles = [surface for i, surface in enumerate(surfaces_in_plane) if not is_circle(len_s_in_plane[i])]
    
    # Crear grupos físicos para círculos
    ph_circ = []
    tags_circ = []
    for i, surface in enumerate(sorted(circles, key=lambda x: x[1][1 - coord])):
        ph = gmsh.model.addPhysicalGroup(2, [surface[0][1]], -1)
        gmsh.model.setPhysicalName(2, ph, f"{layer_name}_circ_{plane}{name}_" + str(i+1))
        ph_circ.append(ph)
        tags_circ.append(surface[0][1])

    rectangle_tag = [ ir[0][1] for ir in rectangles]
    circles_tags = [surface[0][1] for surface in circles]

    ph_rect = gmsh.model.addPhysicalGroup(2, rectangle_tag, -1)
    gmsh.model.setPhysicalName(2, ph_rect, f"{layer_name}_rect_{plane}{name}")
        

    return {"circles": circles_tags,
            "rectangle": rectangle_tag,
            "ph_circ": ph_circ,
            "ph_rect": ph_rect}