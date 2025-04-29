import pandas as pd
def addDisplacement(self,vec):
    newpoints = self.nodes.df.values + vec
    idx = self.nodes.df.index.values
    self.nodes.df = pd.DataFrame(newpoints, 
                                    index=idx, 
                                    columns=["x", "y", "z"])
    # name of index nid
    self.nodes.df.index.name = "nid"