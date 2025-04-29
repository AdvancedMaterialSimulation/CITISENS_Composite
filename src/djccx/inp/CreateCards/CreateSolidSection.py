import numpy as np
from djccx.inp.cards.SolidSectionCard import SolidSectionCard

def CreateSolidSection(self,elset,material,orientation=None):
        # master must be type SurfaceCard

    ssec = SolidSectionCard(elset,material,orientation)
    self.cards = np.append(self.cards,ssec)
    
    return ssec