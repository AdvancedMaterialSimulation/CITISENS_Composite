from djccx.inp.cards.Card import Card
from djccx.inp.cards.NsetCard import NsetCard,NsetCardofNset
class BoundaryCard (Card):
    def __init__(self, nset,dim,displ):
        name = "BOUNDARY"
        super().__init__(name, name)

        # if dim is not 1 or 2 or 3: raise ValueError("dim must be 1, 2 or 3")

        if dim not in [1,2,3]:
            raise ValueError("dim must be 1, 2 or 3")
        


        if isinstance(nset,NsetCard) or isinstance(nset,NsetCardofNset):
            pass
        else:
            raise ValueError("nset must be a NsetCard")
        self.nset  = nset
        self.dim   = dim
        self.displacement = displ
        self.type  = '*BOUNDARY'

    def __repr__(self):
        return self.type + '\n' + self.nset.name + ', ' + str(self.dim) + ', ' + str(self.displacement) + '\n'
    def __str__(self):
        return self.type + '\n' + self.nset.name + ', ' + str(self.dim) + ', ' + str(self.displacement) + '\n'
    
    def print(self):
        return self.type + '\n' + self.nset.name + ', ' + str(self.dim) + ',' + str(self.dim) + ', ' + str(self.displacement) + '\n'

class BoundaryOpNewCard (Card):
    def __init__(self,):
        name = "BOUNDARY"
        super().__init__(name, name)

        self.type  = '*BOUNDARY'

    def print(self):

            return self.type +",OP=NEW" +'\n' 

def read(name,content,cards):
    c = "".join(content)
    c = c.replace('\n','')
    c = c.split(',')
    if c[-1] == '':
        c = c[:-1]
    name = name.replace("\n","").split("BOUNDARY=")[-1]

    if len(c) == 0:
        new_card = BoundaryOpNewCard()
        
    elif len(c) == 4:

        nset  = c[0]
        dim   = int(c[1])
        displacement = float(c[2])

        query = [ inset for inset in cards if inset.name == nset if inset.type == '*NSET']
        if len(query) == 0:
            raise ValueError("Nset not found")
        
        nset = query[0]

        new_card = BoundaryCard(nset,dim,displacement)

    return new_card