from djccx.inp.cards.ElsetCard import ElsetofElsetCard
import numpy as np

def CreateElsetFromElsets(inp_f,elsets,name):
    all = [ element.name for element in elsets]
    elset = ElsetofElsetCard(name,all)
    inp_f.cards = np.append(inp_f.cards,elset)
    return elset