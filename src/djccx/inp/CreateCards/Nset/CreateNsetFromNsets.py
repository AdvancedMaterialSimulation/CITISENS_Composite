from djccx.inp.cards.NsetCard import NsetCardofNset
import numpy as np
def CreateNsetFromNsets(self,name,nsets):


    nset = NsetCardofNset(name,nsets)

    self.cards = np.append(self.cards,nset)

    return nset
# ===========================================
    