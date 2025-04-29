from djccx.inp.cards.Card import Card
class OrientationCard (Card):
    def __init__(self, name, a,b):

        name = name.upper()
        super().__init__(name, name)
        # upcase the name
        self.a = a
        self.b = b

        self.type = '*ORIENTATION'

    def print(self):
        # print the nodes but only in row of 10
        a = self.a
        b = self.b

        return self.type + ', NAME='+self.name + '\n' + \
            str(a[0]) + ',' + str(a[1]) + ',' + str(a[2])  + "," + \
            str(b[0]) + ',' + str(b[1]) + ',' + str(b[2]) 




# =============================================================================


def read(icard,new_cards):
    
    return OrientationCard(icard[1],icard[2:5],icard[5:8])
# =============================================================================