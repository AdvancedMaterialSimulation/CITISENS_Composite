import numpy as np
from djccx.inp.cards.ShellSectionCard import ShellSectionCard

def CreateShellSection(self,elset,material):
        # master must be type SurfaceCard

    ssec = ShellSectionCard(elset,material)
    self.cards = np.append(self.cards,ssec)
    
    return ssec