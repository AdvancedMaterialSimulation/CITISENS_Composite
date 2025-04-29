from djccx.inp.cards.SurfaceInteractionCard import SurfaceInteractionCard
from djccx.inp.cards.ContactCard import ContactCard
import numpy as np
def CreateContacts(self,contacts):

    iSI = SurfaceInteractionCard("ITT","HARD")

    self.cards = np.append(self.cards,iSI)

    surfaces = self.surfaces

    for contact in contacts:

        master = surfaces[contact[0]]
        slave  = surfaces[contact[1]]

        iCC = ContactCard("CC"+master.name_up+slave.name_up,
                          iSI,slave,master)

        self.cards = np.append(self.cards,iCC)



