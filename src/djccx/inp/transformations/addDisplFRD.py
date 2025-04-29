import pandas as pd
def addDisplFRD(self,frd):
    df = frd["data"]

    new_nodes = df[["D1", "D2", "D3"]].values
    new_ind   = df["node"].values

    df_nodes = pd.DataFrame(new_nodes, columns=["x", "y", "z"])
    df_nodes["nid"] = new_ind
    df_nodes["nid"] = df_nodes["nid"].astype(int)
    df_nodes = df_nodes.set_index("nid")

    self.nodes.df = self.nodes.df.add(df_nodes,fill_value=0)

    return self