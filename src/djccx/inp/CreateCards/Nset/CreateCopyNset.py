import numpy as np
import pandas as pd
def CreateCopyNset(self,nameset,nameset_copy,vec):

    rep_nset = self.select(nameset,"nset")
    nodes_df    = self.nodes.df.loc[rep_nset.id_nodes]
    nodes_rep   = nodes_df.values.copy() + vec
    id_rep_old  = nodes_df.index.values.copy()

    last_id     = np.max(self.nodes.df.index.values)
    id_rep      = id_rep_old + last_id

    df_rep = pd.DataFrame(nodes_rep,columns=["x","y","z"])
    df_rep["nid"] = id_rep
    # set nid as index
    df_rep = df_rep.set_index("nid")

    self.nodes.df = pd.concat([self.nodes.df,df_rep])
    # create a nset with the new nodes
    inset_rep = self.CreateNsetFromIds(id_rep,nameset_copy)

    return inset_rep

