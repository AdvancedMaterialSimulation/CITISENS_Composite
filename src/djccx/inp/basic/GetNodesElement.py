def GetNodesElement(self,element):
    nid = self.nodes.df.index.values
    ide = element.eid
    # get the position of the every element of ide in nid
    index_nodes = [ i for i in nid if i in ide]
    # get the nodes 
    nodes =  self.nodes.df.iloc[index_nodes]
    return nodes