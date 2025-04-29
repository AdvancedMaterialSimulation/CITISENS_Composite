from djccx.inp.cards.Step.StepCard import StepCard
import numpy as np

def CreateStaticStep(self,nlgeom=False):
    step = StepCard([],nlgeom=nlgeom)
    self.cards = np.append(self.cards,step)

    return step