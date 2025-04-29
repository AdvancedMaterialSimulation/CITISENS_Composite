from djccx.inp.cards.Card import Card
from djccx.inp.cards.MaterialCard import MaterialCard
from djccx.inp.cards.ElsetCard import ElsetCard,ElsetofElsetCard

class ShellSectionCard (Card):
    def __init__(self, elset, material,thinckness=0.1):
        name = "SHELL_SECTION"
        super().__init__(name, name)

        if not (isinstance(elset, ElsetCard) or isinstance(elset, ElsetofElsetCard)):
            raise Exception("elset must be an ElsetCard or ElsetofElsetCard")
        if not isinstance(material, MaterialCard):
            raise Exception("material must be a MaterialCard")
        
        self.elset     = elset
        self.material  = material
        self.thickness = thinckness
        self.type = '*SHELLSECTION'

    def print(self):
        # print the nodes but only in row of 10
        return '*SHELL SECTION, ELSET=' + self.elset.name_up + ', MATERIAL=' + self.material.name_up + '\n' + str(self.thickness)


# =============================================================================


def read(name,new_cards,verbose=False):

    printw = lambda x: print(x) if verbose else None
    opt = name.replace("*SHELLSECTION,","").split(",")
    opt = [i.split("=") for i in opt]
    opt = {i[0]:i[1] for i in opt}

    elset = [ icard for icard in new_cards
                if (isinstance(icard,ElsetCard) or isinstance(icard,ElsetofElsetCard))
                if icard.name == opt["ELSET"]]

    material = [ icard for icard in new_cards
                if isinstance(icard,MaterialCard)
                if icard.name == opt["MATERIAL"]]

    if len(elset) == 0:
        printw("No existe el elset: "+opt["ELSET"])
        printw("*SHELL SECTION")

        return None
    if len(elset) > 1:
        printw("Existe mas de un elset: "+opt["ELSET"])
        printw("*SHELL SECTION")

        return None
    if len(material) == 0:
        printw("No existe el material: "+opt["MATERIAL"])
        printw("*SHELL SECTION")

        return None
    if len(material) > 1:
        printw("Existe mas de un material: "+opt["MATERIAL"])
        printw("*SHELL SECTION")

        return None

    elset  = elset[0]
    material = material[0]

    new_card = ShellSectionCard(elset,material)

    return new_card