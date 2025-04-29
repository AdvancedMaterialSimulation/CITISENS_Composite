from djccx.inp.cards.Card import Card
from djccx.inp.cards.MaterialCard import MaterialCard
from djccx.inp.cards.ElsetCard import ElsetCard,ElsetofElsetCard
from djccx.inp.cards.OrientationCard import OrientationCard

class SolidSectionCard (Card):
    def __init__(self, elset, material,orientation=None):
        name = "SOLID_SECTION"
        super().__init__(name, name)

        if not (isinstance(elset, ElsetCard) or isinstance(elset, ElsetofElsetCard)):
            raise Exception("elset must be an ElsetCard or ElsetofElsetCard")
        if not isinstance(material, MaterialCard):
            raise Exception("material must be a MaterialCard")
        
        if orientation is not None:
            if not isinstance(orientation, OrientationCard):
                raise Exception("orientation must be an OrientationCard")
            self.orientation = orientation
        else:
            self.orientation = None

        self.elset     = elset
        self.material  = material
        self.type = '*SOLIDSECTION'

    def print(self):
        # print the nodes but only in row of 10
        if self.orientation is not None:
            return '*SOLID SECTION , ELSET=' + self.elset.name_up + ', MATERIAL=' + self.material.name_up + ', ORIENTATION=' + self.orientation.name_up
        else:
            return '*SOLID SECTION , ELSET=' + self.elset.name_up + ', MATERIAL=' + self.material.name_up


# =============================================================================


def read(name,new_cards,verbose=False):

    printw = lambda x: print(x) if verbose else None
    opt = name.replace("*SOLIDSECTION,","").split(",")
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
        printw("*SOLID SECTION")

        return None
    if len(elset) > 1:
        printw("Existe mas de un elset: "+opt["ELSET"])
        printw("*SOLID SECTION")

        return None
    if len(material) == 0:
        printw("No existe el material: "+opt["MATERIAL"])
        printw("*SOLID SECTION")

        return None
    if len(material) > 1:
        printw("Existe mas de un material: "+opt["MATERIAL"])
        printw("*SOLID SECTION")

        return None

    elset  = elset[0]
    material = material[0]

    new_card = SolidSectionCard(elset,material)

    return new_card