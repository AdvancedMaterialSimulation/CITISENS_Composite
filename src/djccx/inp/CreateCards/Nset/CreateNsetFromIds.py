import numpy as np
from djccx.inp.cards.NsetCard import NsetCard

def CreateNsetFromIds(self,id_values_list,name=None):

    id_values_list = [int(i) for i in id_values_list]
    id_values_list = np.array(id_values_list).astype(int)
    nset = NsetCard(name, id_values_list)

    self.cards = np.append(self.cards,nset)

    # add to cards and nsets
    return nset