from djccx.inp.cards.ElsetCard import ElsetofElsetCard
import numpy as np
def CreateElsetAll(self):

    all = [ element.options["ELSET"] for element in self.elements]

    elset = ElsetofElsetCard('ALL',all)
    self.cards = np.append(self.cards,elset)
    return elset