
from djccx.inp.cards.MaterialCard import MaterialCard,ElasticEngineeringCard
import numpy as np
def CreateElasticEngineeringMaterial(self,name,E1,E2,E3,nu12,nu13,nu23,G12,G13,G23):

    iEC = ElasticEngineeringCard(E1,E2,E3,nu12,nu13,nu23,G12,G13,G23)

    imat =  MaterialCard(name,[iEC])

    self.cards = np.append(self.cards,imat)

    return imat


