from djccx.inp.cards.Card import Card

class DloadCard (Card):
    def __init__(self, elset,face,preassure):

        name = "DLOAD"
        super().__init__(name, name)

        self.elset = elset
        self.face   = face
        self.preassure = preassure
        self.type  = '*DLOAD'

    def print(self):
        return self.type + '\n'  + \
            self.elset.name + ', P' + str(self.face+1) +"," + str(self.preassure) + '\n'
    
def read(name,content,cards):

    c = "".join(content)
    c = c.replace('\n','')
    c = c.split(',')
    if c[-1] == '':
        c = c[:-1]
    name = name.replace("\n","").split("DLOAD=")[-1]
    elset = c[0]
    face = c[1]
    preassure = c[2]

    query = [ inset for inset in cards if inset.name == elset if inset.type == '*ELSET']
    if len(query) == 0:
        raise ValueError("Elset not found")
    
    elset = query[0]
    new_card = DloadCard(elset,face,preassure)

    return new_card