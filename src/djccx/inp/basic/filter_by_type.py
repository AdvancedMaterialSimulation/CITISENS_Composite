types = ["T3D3","CPS6","C3D10"]
def filter_by_type(self,dim,replace=False):
    id_volumen = [j for j, card in enumerate(self.cards) 
                    if card.options != {} 
                    if card.options["TYPE"] == types[dim-1]]

    cards_select = self.cards[id_volumen]
    if replace:
        self.cards = cards_select
        self.elements = [card for card in self.cards 
                            if card.type == '*ELEMENT']

    return cards_select