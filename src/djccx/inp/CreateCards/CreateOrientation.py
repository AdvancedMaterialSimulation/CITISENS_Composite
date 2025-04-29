import numpy as np
from djccx.inp.cards.OrientationCard import OrientationCard

def CreateOrientation(self,name,a,b):
        # master must be type SurfaceCard

    ssec = OrientationCard(name, a,b)
    self.cards = np.append(self.cards,ssec)
    
    return ssec