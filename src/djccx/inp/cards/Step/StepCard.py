from djccx.inp.cards.Card import Card
from djccx.inp.cards.Step.Boundary import BoundaryCard, read as parse_boundary
from djccx.inp.cards.Step.CloadCard import CloadCard, read as parse_cload
from djccx.inp.cards.Step.DloadCard import DloadCard, read as parse_dload
import numpy as np
class StepCard (Card):
    def __init__(self, cards,nlgeom=False):
        name = "STEP"

        super().__init__(name, name)
        self.type = "*STEP"
        self.nlgeom = nlgeom
        self.cards = cards
        self.elsets_print = ["ALL"]
        self.output = {
            "node":{
                "RF":True,
                "U":True
            },
            "element":{
                "S":True,
                "E":True
            },
            "contact":{
                "CDIST":False,
                "CSTR":False,
                "PCON":False
            },
            "elprint":{
                "EVOL":True,
            }
        }

    def print(self):
        
        lines = "*STEP\n*STATIC\n"
        for card in self.cards:
            lines = lines + card.print()

        node_file = ["node","element","contact"]
        card_name = ["*NODE FILE","*EL FILE","*CONTACT FILE"]
        for i, file in enumerate(node_file):
            
            lines = lines + card_name[i] + "\n"
            for key in self.output[file]:
                if self.output[file][key]:
                    lines = lines + key  + ", "
            lines = lines[:-1] + "\n"

        # el print
        for elset in self.elsets_print:

            lines = lines + "*EL PRINT, ELSET=" + elset + "\n"
            for key in self.output["elprint"]:
                if self.output["elprint"][key]:
                    lines = lines + key  + ", "
            lines = lines[:-1] + "\n"


        lines = lines + "*END STEP\n"
        return lines
    

    def CreateBoundary(self,nset,dim,displ):
        new_card = BoundaryCard(nset,dim,displ)
        self.cards = np.append(self.cards,new_card)
        return new_card
    
    def CreateCload(self,nset,dim,value):
        new_card = CloadCard(nset,dim,value)
        self.cards = np.append(self.cards,new_card)
        return new_card
    
    def CreateDload(self,elset,face,value):
        new_card = DloadCard(elset,face,value)
        self.cards = np.append(self.cards,new_card)
        return new_card

    def CreateDloadSurface(self,surfaces,preassure):

        new_cards = []
        for i,elset in enumerate(surfaces.elsets):
            new_card = DloadCard(elset,i,preassure)
            self.cards = np.append(self.cards,new_card)
            new_cards.append(new_card)
        return new_card

# =============================================================================
def read(step_lines,new_cards):


    # remove \n
    name = step_lines[0].replace("\n","")
    # split by ","
    name_split  = name.split(",")

    if len(name_split) > 1:
        options = name_split[1:]    
        nlgeom = True if 'NLGEOM' in options else False
    else:
        nlgeom = False

    type = step_lines[1]
    content = step_lines[2:-1]


    index = [i for i, line in enumerate(content) if line.startswith('*')]
    # add the last line
    index.append(len(content))

    cards = [content[index[i]:index[i+1]] for i in range(len(index)-1)]

    new_cards_steps = []
    for icard in cards:
        name    = icard[0].upper().replace(" ","").replace("\n","")
        content_loop = icard[1:]

        if name.startswith('*BOUNDARY'):
            new_card = parse_boundary(name, content_loop,new_cards)
        elif name.startswith('*CLOAD'):
            new_card = parse_cload(name, content_loop,new_cards)
        elif name.startswith('*DLOAD'):
            new_card = parse_dload(name, content_loop,new_cards)
        else:
            continue
        new_cards_steps.append(new_card)


    return StepCard(new_cards_steps,nlgeom)