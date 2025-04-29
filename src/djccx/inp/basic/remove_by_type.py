import numpy as np

types = ["T3D3","CPS6","C3D10"]

def remove_by_type(self,dim):
    id_elements = [j for j, card in enumerate(self.cards) 
                        if card.type         == '*ELEMENT' 
                        if card.options["TYPE"] == types[dim-1]]

    idx = np.arange(len(self.cards))
    idx = np.delete(idx,id_elements)

    cards_select = self.cards[idx]

    self.cards = cards_select

    return self