from djccx.inp.cards.Card import Card
from djccx.inp.cards.SurfaceCard import SurfaceCard
from djccx.inp.cards.SurfaceInteractionCard import SurfaceInteractionCard

class ContactCard (Card):

    def __init__(self, name, SurfaceInteraction, slave,master):
        super().__init__(name, name)

        self.master = master
        self.slave  = slave
        self.SurfaceInteraction = SurfaceInteraction
        self.type = '*CONTACTPAIR'

    def print(self):
        # print the nodes but only in row of 10
        return  '*CONTACT PAIR, INTERACTION=' +\
               self.SurfaceInteraction.name_up + \
                ',TYPE=SURFACE TO SURFACE\n' +\
               self.slave.name_up + ', ' + self.master.name_up + '\n' 

# =============================================================================
def read(name,content,new_cards,verbose=False):
    # name = "*CONTACT PAIR, INTERACTION=INT1,TYPE=SURFACE TO SURFACE"
    # content = "SURF1, SURF2"
    # new_cards = [SurfaceCard, SurfaceInteractionCard]

    printw = lambda x: print(x) if verbose else None

    opt = name.replace("*CONTACTPAIR,","").split(",")
    opt = [i.split("=") for i in opt]
    opt = {i[0]:i[1] for i in opt}

    interaction = opt["INTERACTION"]
    cint = [ inter for inter in new_cards 
            if isinstance(inter,SurfaceInteractionCard)
            if inter.name == interaction]

    if len(cint) == 0:
        printw("No existe la interaccion: "+interaction)
        return None
    if len(cint) > 1:
        printw("Existe mas de una interaccion: "+interaction)
        return None

    cint = cint[0]
    ncontent = content[0].replace("\n","").replace(" ","").split(",")


    slave = [ icard for icard in new_cards
                if isinstance(icard,SurfaceCard)
                if icard.name == ncontent[0]]

    master = [ icard for icard in new_cards
                if isinstance(icard,SurfaceCard)
                if icard.name == ncontent[1]]
    
    if len(slave) == 0:
        printw("No existe la superficie: "+ncontent[0])
        printw("*CONTACT PAIR")
        return None
    if len(slave) > 1:
        printw("Existe mas de una superficie: "+ncontent[0])
        printw("*CONTACT PAIR")

        return None
    if len(master) == 0:
        printw("No existe la superficie: "+ncontent[1])
        printw("*CONTACT PAIR")

        return None
    if len(master) > 1:
        printw("Existe mas de una superficie: "+ncontent[1])
        printw("*CONTACT PAIR")
        return None

    slave  = slave[0]
    master = master[0]
    name = "CONTACT"
    new_card = ContactCard(name,cint,slave,master)
    return new_card