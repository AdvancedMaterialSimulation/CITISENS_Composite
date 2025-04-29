import numpy as np

from djccx.tools.el2face import el2face


def select_faces(inp_obj,surf,all_elements,
                 nodes=None): 
    """   
    Inputs:
    -------
    * inp_obj: object of class Inp
    * surf: object of class Surface
    * elem: object of class Element
    * nodes: object of dataframe nid,x,y,z
    """
    if nodes is None:
        nodes = inp_obj.nodes.df

    nodes = nodes.copy()
    nodes["real_index"] = np.arange(0,len(nodes))

    all_faces = []
    for k in range(4):

        ide     = surf.elsets[k].id_elements
        el_data = all_elements.loc[ide]
        
        el_data = el_data[[0,1,2,3]]

        el_data_real_index = [ nodes.loc[el_data.iloc[i].values].real_index.values 
                               for i in range(len(el_data))]

        for i in range(len(el_data_real_index)):
            faces = el2face(el_data_real_index[i],nface=k)
            all_faces.extend(faces)

    return all_faces