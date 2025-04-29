from djccx.inp.cards.NsetCard import NsetCardofNset
import numpy as np
def CreateNsetFromLabels(self,name,labels):


    # to this the labels must be a list of strings
    # must be exist in the model


    names = [nset.name for nset in self.nsets]

    if not all([label in names for label in labels]):
        raise Exception("labels must be a list of strings that exist in the model")
    
    # name of the new nset
    # comprueba que no exista
    if name in names:
        print(names)
        raise Exception("name of the new nset already exist")

    nset = NsetCardofNset(name,labels)

    self.cards = np.append(self.cards,nset)

    