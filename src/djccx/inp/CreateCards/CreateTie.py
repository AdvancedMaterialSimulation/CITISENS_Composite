from djccx.inp.cards.TieCard import TieCard
import numpy as np

def CreateTie(self,name,slave,master,type="surface"):
    # master must be type SurfaceCard
    if type not in ["surface","nset"]:
        raise Exception("type must be surface or nset")

    master = self.select(master.name,"surface")
    slave  = self.select(slave.name,type)

    tie = TieCard(name,slave,master)
    self.cards = np.append(self.cards,tie)
    
    return tie