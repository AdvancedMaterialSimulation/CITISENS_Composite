from djccx.inp.cards.EquationCard import EquationCard
import numpy as np
def AddEquation(self,nset1,nset2,type_eq="point2point",dims=[1,2,3],nodes=None):

    nset1 = self.select(nset1,"nset")
    nset2 = self.select(nset2,"nset")

    equation = EquationCard("EQUATION",nset1,nset2,type_eq=type_eq,dims=dims,nodes=nodes)

    self.cards = np.append(self.cards,equation)

    # add to cards and nsets
    return equation