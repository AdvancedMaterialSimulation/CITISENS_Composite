from djccx.inp.cards.TransformCard import TransformCard
from djccx.inp.cards.NsetCard import NsetCard,NsetCardofNset
import numpy as np

def CreateTransform(self,nset,r1,r2):

    # r1 must be array of 3 elements
    # r2 must be array of 3 elements

    # validation
    if type(r1) is not np.ndarray:
        raise Exception('r1 must be np.ndarray')
    if type(r2) is not np.ndarray:
        raise Exception('r2 must be np.ndarray')
    
    if len(r1) != 3:
        raise Exception('r1 must have 3 elements')
    if len(r2) != 3:
        raise Exception('r2 must have 3 elements')
    
    # nset must be a NsetCard or NsetCardofNset
    if not isinstance(nset,NsetCard) and not isinstance(nset,NsetCardofNset):
        raise Exception('nset must be a NsetCard')

    transform = TransformCard(nset,r1,r2)
    self.cards = np.append(self.cards,transform)
    
    return transform