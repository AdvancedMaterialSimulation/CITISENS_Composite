from djccx.inp.cards.Card import Card

class ElasticCard (Card):
    def __init__(self, E,nu):

        name = "ELASTIC"
        super().__init__(name, name)

        self.E  = E
        self.nu = nu
        self.type = '*ELASTIC'

    def print(self):

        return "*ELASTIC\n{},{}\n".format(self.E,self.nu)

class ElasticEngineeringCard (Card):

    def __init__(self, E1,E2,E3,nu12,nu13,nu23,G12,G13,G23):

        name = "ELASTIC"
        super().__init__(name, name)

        self.E1  = E1
        self.E2  = E2
        self.E3  = E3
        self.nu12 = nu12
        self.nu13 = nu13
        self.nu23 = nu23
        self.G12 = G12
        self.G13 = G13
        self.G23 = G23

        self.type = '*ELASTIC,TYPE=ENGINEERING CONSTANTS'

    def print(self):

        return "*ELASTIC,TYPE=ENGINEERING CONSTANTS\n{}, {}, {}, {}, {}, {}, {}, {}\n{},273.15".format(
            self.E1,self.E2,self.E3,
            self.nu12,self.nu13,self.nu23,
            self.G12,self.G13,self.G23)
    

class DensityCard (Card):
    def __init__(self, rho):
        name = "DENSITY"
        super().__init__(name, name)

        self.rho  = rho
        self.type = '*DENSITY'

    def print(self):
        return "*DENSITY\n{}\n".format(self.rho)

class MaterialCard (Card):
    def __init__(self, name, cards):

        # name capitalized
        name = name.upper()
        super().__init__(name, name)
        self.type = "*MATERIAL"

        self.cards = cards

    def print(self):
        
        lines = "*MATERIAL, NAME={}\n".format(self.name)
        for card in self.cards:
            lines = lines + card.print()
        return lines
    

# =============================================================================
def read(name,content,cards,index):
    opts = name.split('=')
    name = opts[1]

    posible_cards = ['*ELASTIC','*EXPANSION',
                     '*CONDUCTIVITY',"*SPECIFICHEAT",
                     "*DENSITY"]

    for i in range(index+1,len(cards)):
        
        pc = False
        for iposi in posible_cards:
            if cards[i][0].startswith(iposi):
                pc = True
                break
        if not pc:
            break

    select_cards = cards[(index+1):(i+1)]
    select_cards = cards[(index+1):(i)]
    
    for i in range(len(select_cards)):
        select_cards[i][0] = select_cards[i][0].replace("\n","")
        select_cards[i][1] = select_cards[i][1].replace("\n","")

    implemented_cards = ["*ELASTIC","*DENSITY"]

    select_cards = [card for card in select_cards
                        if card[0].split(',')[0] in implemented_cards]
    
    new_cards = []
    for icard in select_cards:
        if icard[0].startswith('*ELASTIC'):
            E,nu = icard[1].split(',')
            E  = float(E)
            nu = float(nu)
            new_card = ElasticCard(E,nu)
        elif icard[0].startswith('*DENSITY'):
            rho = float(icard[1])
            new_card = DensityCard(rho)
        new_cards.append(new_card)

    material_card = MaterialCard(name,new_cards)
    return material_card