import numpy as np
from djccx.inp.cards.ElsetCard   import ElsetCard
from djccx.inp.cards.SurfaceCard import SurfaceCard


def vecnormal(matrix):
    # matrix es una matriz de 3x3
    v1 = matrix[1, :] - matrix[0, :]
    v2 = matrix[2, :] - matrix[0, :]
    v =  -np.cross(v1, v2)
    return v / np.linalg.norm(v)


def compute_faces_all(tetra):
    return np.array([tetra[[0, 1, 2, 4, 5, 6]],
                     tetra[[0, 3, 1, 7, 8, 4]],
                     tetra[[1, 3, 2, 9, 5, 8]],
                     tetra[[2, 3, 0, 7, 6, 9]]])


def compute_faces(tetra):
    return np.array([tetra[[0, 1, 2]],
                     tetra[[0, 3, 1]],
                     tetra[[1, 3, 2]],
                     tetra[[2, 3, 0]]])


list_id = np.arange(1, 5)

def ComputeFaceOrder(element_face, nset,select_element):
    id = set(nset.id_nodes)
    # element_face es una lista de 4 caras (triangulos)
    # element_face es una matriz de 4x3
    r = [set(iel).issubset(id) for iel in element_face]

    r = list_id[r]

    if len(r) == 0:
        return None
    else:

        element_face = compute_faces_all(select_element)
        r = [set(iel).issubset(id) for iel in element_face]
        r = list_id[r]

        return r
    
def addSurface(inp_f,element,nset,name):

    # En este caso tenemos 3 cartas *ELEMENT
    # debido a que el hilo se ha dividido en 3 partes
    # es necesario unirlas en una sola carta *ELEMENT
    # eliminamos las cartas *ELEMENT que ya no son necesarias
    # sus elementos se han unido en la primera carta *ELEMENT
    #
    select_elements = element.elements
    id_elements     = element.eid
    # Creamos una lista de caras para cada elemento
    element_faces = [compute_faces(select_elements[i])
                    for i in range(len(select_elements))]

    # Para cada elemento calculamos la cara que apunta hacia el exterior
    # si no tiene cara que apunte hacia el exterior, se devuelve None

    FaceOrder = [ ComputeFaceOrder(element_faces[i], 
                                   nset,
                                   select_elements[i]) 
                 for i in range(len(element_faces)) ]
    
    # Ordenamos los elementos por cara exterior
    index_Faces_4 = [  [  i for i, iFO in enumerate(FaceOrder) 
                          if iFO is not None
                          if j   in    iFO   ] 
                          for j in range(1, 5)]
    
    # Obtenemos los id de los elementos
    id_Faces_4 = [[id_elements[i] 
                   for i in index_Faces_4[j]] 
                   for j in range(4)]
    name = name.upper()
    # Creamos los elsets para cada cara
    elsets = [ElsetCard("ELSET_SURFACE_"+name+"_"+str(i+1), id_Faces_4[i])
            for i in range(4)]
    # Añadimos los elsets al archivo inp
    inp_f.cards = np.append(inp_f.cards, elsets)

    # Creamos la superficie con los elsets  
    #  Es necesario que esten ordenados, 
    # Elset1 (Cara 1 hacia el exterior), 
    # Elset2 (Cara 2 hacia el exterior), etc
    isurface = SurfaceCard(name, elsets)
    inp_f.cards = np.append(inp_f.cards, isurface)
    
