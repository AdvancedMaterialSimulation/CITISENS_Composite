from djccx.inp.cards.Card import Card

class CloadCard (Card):
    def __init__(self, nset,dim,value):

        name = "CLOAD"
        super().__init__(name, name)

        self.nset  = nset
        self.dim   = dim
        self.value = value
        self.type  = '*CLOAD'

    def print(self):
        return self.type + '\n' + self.nset.name + ', ' + self.dim + ', ' + self.value

class CloadOpNewCard (Card):
    def __init__(self,):
        name = "CLOAD"
        super().__init__(name, name)

        self.type  = '*CLOAD'

    def print(self):
        return self.type +",OP=NEW" +'\n'

def read(name,content,cards):
    c = "".join(content)
    c = c.replace('\n','')
    c = c.split(',')
    if c[-1] == '':
        c = c[:-1]
    
    name = name.replace("\n","").split("CLOAD=")[-1]
    
    if len(c) == 0:
        new_card = CloadOpNewCard()
    elif len(c) == 1:
        nset = c[0]
        dim = c[1]
        value = c[2]

        query = [ inset for inset in cards if inset.name == nset if inset.type == '*NSET']
        if len(query) == 0:
            raise ValueError("Nset not found")
        
        nset = query[0]
        new_card = CloadCard(name,nset,dim,value)

    return new_card