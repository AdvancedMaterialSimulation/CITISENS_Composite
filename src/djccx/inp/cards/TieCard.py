from djccx.inp.cards.Card import Card
from djccx.inp.cards.SurfaceCard import SurfaceCard,SurfaceNodeCard

class TieCard (Card):
    def __init__(self, name, slave, master):
        super().__init__(name, name)

        self.master = master
        self.slave  = slave
        self.type = '*TIE'

    def print(self):
        # print the nodes but only in row of 10
        return self.type    + ', NAME=' +\
               self.name_up + ',position tolerance=0.1\n' +\
               self.slave.name_up + ', ' + self.master.name_up

    def restart_index_element(self, id_elements):
        self.id_elements = self.id_elements + id_elements

        return self


# =============================================================================



def read(name,content,new_cards,verbose=False):
    printw = lambda x: print(x) if verbose else None
    opt = name.replace("*TIE,","").split(",")
    opt = [i.split("=") for i in opt]
    opt = {i[0]:i[1] for i in opt}
    ncontent = content[0].replace("\n","").replace(" ","").split(",")

    slave = [ icard for icard in new_cards
                if ( isinstance(icard,SurfaceCard)  or
                     isinstance(icard,SurfaceNodeCard))
                if icard.name == ncontent[0]]

    master = [ icard for icard in new_cards
                if isinstance(icard,SurfaceCard)
                if icard.name == ncontent[1]]

    if len(slave) == 0:
        printw("No existe la superficie: "+ncontent[0])
        printw("*TIE")

        return None
    if len(slave) > 1:
        printw("Existe mas de una superficie: "+ncontent[0])
        printw("*TIE")

        return None
    if len(master) == 0:
        printw("No existe la superficie: "+ncontent[1])
        printw("*TIE")

        return None
    if len(master) > 1:
        printw("Existe mas de una superficie: "+ncontent[1])
        printw("*TIE")

        return None

    slave  = slave[0]
    master = master[0]

    new_card = TieCard(opt["NAME"],slave,master)

    return new_card