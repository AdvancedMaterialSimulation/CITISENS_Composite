import numpy as np
import pandas as pd

def CreateNsetCopy(inp_file,rep_nset,label,vec):
    nodes_df    = inp_file.nodes.df.loc[rep_nset.id_nodes]
    nodes_rep   = nodes_df.values.copy() + vec
    id_rep_old  = nodes_df.index.values.copy()
    last_id     = np.max(inp_file.nodes.df.index.values)
    id_rep      = id_rep_old + last_id
    # add type col 
    # create a df with the new nodes
    df_rep = pd.DataFrame(nodes_rep,columns=["x","y","z"])
    df_rep["nid"] = id_rep
    # set nid as index
    df_rep = df_rep.set_index("nid")

    inp_file.nodes.df = pd.concat([inp_file.nodes.df,df_rep])

    # create a nset with the new nodes
    inset_rep = inp_file.CreateNsetFromIds(id_rep,label)
    
    return inset_rep