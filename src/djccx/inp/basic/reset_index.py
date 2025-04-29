def reset_index(self,last_node_id,last_ele_id):

    for element in self.elements:
        element.restart_index_nodes(last_node_id)
        element.restart_index_element(last_ele_id)
    #        
    for nset in self.nsets:
        nset.restart_index_nodes(last_node_id)
    
    for elset in self.elsets:
        elset.restart_index_element(last_ele_id)
    
    return self