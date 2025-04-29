
from djccx.inp.cards.MaterialCard import MaterialCard,ElasticCard
import numpy as np
def CreateElasticMaterial(self,name,E,nu):

    iEC = ElasticCard(E,nu)

    imat =  MaterialCard(name,[iEC])

    self.cards = np.append(self.cards,imat)

    return imat


