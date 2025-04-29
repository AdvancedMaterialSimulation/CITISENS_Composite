
from scipy.spatial import distance as dist
import numpy as np
import pandas as pd
def SetUniqueNodes(inp_f):
    matrix_nodes = inp_f.nodes.df.values

    # distancia entre nodos 
    D = dist.squareform(dist.pdist(matrix_nodes))
    # buscamos los nodos que estan muy cerca == 0
    # ids = [ 2+j+np.where(D[j,(j+1):] ==0)[0] 
    #        for j in range(D.shape[0]-1) ]
    
    # cerca 
    ids = [ 2+j+np.where(D[j,(j+1):] < 1e-2)[0]
              for j in range(D.shape[0]-1) ]

    nodos_replicados = []
    for i in range(len(ids)):
        if len(ids[i]) > 0:

            list_el = ids[i].tolist()
            list_el.insert(0, i+1)
            nodos_replicados.append(list_el)

    # identificamos lo nodos a eliminar (estan replicados )
    id_nodes_rm = np.concatenate([iids[1:]
                                for iids in nodos_replicados if len(iids) > 0])
    id_nodes_rm = np.unique(id_nodes_rm)
    inp_f.nodes.df = inp_f.nodes.df.drop(id_nodes_rm)


    # replace nodes
    for k in range(len(nodos_replicados)):
        keep_node = nodos_replicados[k][0]
        rm_nodes  = nodos_replicados[k][1:]

        for element in inp_f.elements:
            el_mt = element.elements
            for irm in rm_nodes:
                element.elements[el_mt == irm] = keep_node
                
                index_df = element.df.index
                cols = element.df.columns
                df_new = pd.DataFrame(element.elements, 
                                      columns=cols, 
                                      index=index_df)
                element.df = df_new
        for nset in inp_f.nsets:
            for irm in rm_nodes:
                nset.id_nodes[nset.id_nodes == irm] = keep_node
