def setResults(self,frd,onlyfrd=False):

    # ms = ['D1', 'D2', 'D3', 'SXX', 'SYY', 'SZZ', 'SXY', ...]
    ms = frd["data"].keys().values[4:]
    
    # nodes is a dataframe with the nodes and the results
    nodes = self.nodes.df.copy()
    if onlyfrd:
        indx_frd = frd["data"]["node"].values
        nodes = nodes.loc[indx_frd]
    # nodes has a [x, y, z] with index = nid
    # Add new columns to the nodes dataframe
    # ms = ['D1', 'D2', 'D3', 'SXX', 'SYY', 'SZZ', 'SXY', ...]
    for im in ms:
        nodes[im] = frd["data"][im]
        
    self.frd = nodes

    return nodes
