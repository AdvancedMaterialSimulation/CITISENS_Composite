from djccx.inp.cards.Card import Card
import numpy  as np
class NsetCard (Card):
    def __init__(self, name, id_nodes):

        name = name.upper()
        super().__init__(name, id_nodes)
        # upcase the name
        self.id_nodes = id_nodes
        self.type = '*NSET'

    def radius(self,nodes):
        # * Input:
        #   - nodes: NodeCard
        # Se calcula el radio de un circulo que contenga 
        # todos los nodos
        nodes_df = nodes.df.loc[self.id_nodes]
        center   = nodes_df.mean(axis=0)
        d2center = np.linalg.norm(nodes_df.values -\
                                        center.values,
                                        axis=1)
        radius = np.max(d2center)
        return radius
    def print(self):
        # print the nodes but only in row of 10
        line = ''
        for i, node in enumerate(self.id_nodes):
            line += str(node) + ','
            if i % 10 == 0 and i != 0:
                line += '\n'
        line = line[:-1]
        name_up = self.name_up.replace("\n", "")
        return self.type + ', NSET=' + name_up + '\n' + line 

    def GetNodes(self,nodes):
        return nodes.df.loc[self.id_nodes]

    def restart_index_nodes(self, id_node_start):
        self.id_nodes = self.id_nodes + id_node_start
        return self


# =============================================================================
class NsetCardofNset (Card):

    @property
    def id_nsets(self):
        names = [nset.name for nset in self.nsets]
        return names
    
    def __init__(self, name, nsets):
        super().__init__(name, name)

        self.nsets = nsets
        self.type = '*NSET'




    def print(self):
        # print the nodes but only in row of 10
        line = ''
        for i, node in enumerate(self.id_nsets):
            line += str(node) + ','
            if i % 10 == 0 and i != 0:
                line += '\n'
        line = line[:-1]
        name_up = self.name_up.replace("\n", "")
        return self.type + ', NSET=' + name_up + '\n' + line 

# =============================================================================


def read(icard,new_cards):
    id_nodes = icard[1:]
    # remove the \n
    id_nodes = [i.replace('\n','') for i in id_nodes]
    # join the list
    id_nodes = ''.join(id_nodes).split(',')
    # remove empty elements
    id_nodes = [i for i in id_nodes 
            if i != '']                    
    # to int 
    name = icard[0].replace(" ","").split("=")
    name = name[1]
    try:
        id_nodes = np.array(id_nodes,dtype=int)

        new_card = NsetCard(name,id_nodes)
    except:
        nsets_names = id_nodes
        
        all_nsets = [card.name for card in new_cards if card.type == '*NSET']

        nsets = []
        for iname in nsets_names:
            if iname in all_nsets:
                nset = [card for card in new_cards if card.name == iname][0]
                nsets.append(nset)
            else:
                raise ValueError('The reference nset does not exist, in the nset: '+name)
            
        nsets = np.array(nsets)
        new_card = NsetCardofNset(name,nsets)

    return new_card