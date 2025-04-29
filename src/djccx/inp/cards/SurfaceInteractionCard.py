from djccx.inp.cards.Card import Card


class SurfaceInteractionCard (Card):
    def __init__(self, name, type):
        super().__init__(name, name)
        self.type = "*SURFACEINTERACTION"
        self.interaction = type
    def print(self):
        return '*SURFACE INTERACTION, NAME=' + self.name_up  + "\n*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=HARD\n"


# =============================================================================

def read(name,cards,index,verbose=False):
   
    printw = lambda x: print(x) if verbose else None    
    next_card = cards[index+1]
    next_name = next_card[0].upper().replace(" ","").replace("\n","")
    if not next_name.startswith("*SURFACEBEHAVIOR,"):
        printw("* SURFACE INTERACTION must be followed by *SURFACEBEHAVIOR")
        return None
    next_name = next_name.replace("*SURFACEBEHAVIOR,,","")
    opt_surf = next_name.split("=")
    type = opt_surf[1]
    name = name.replace("*SURFACEINTERACTION,","")
    name = name.split("=")
    name = name[1]
    new_card = SurfaceInteractionCard(name,type)
    return new_card