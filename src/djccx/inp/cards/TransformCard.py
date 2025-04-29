# *TRANSFORM, NSET=bot, TYPE=C
# 0,0,0,0,0,1

from djccx.inp.cards.Card import Card
import numpy as np
class TransformCard (Card):
    def __init__(self, nset,r1,r2,type="C"):

        name = "*TRANSFORM" 
        super().__init__(name, name)
        # upcase the name
        self.type = '*TRANSFORM'
        self.typetransform = type
        self.nset = nset
        self.r1 = r1
        self.r2 = r2

    def print(self):
        # print the nodes but only in row of 10
        x1 = str(self.r1[0])
        y1 = str(self.r1[1])
        z1 = str(self.r1[2])
        x2 = str(self.r2[0])
        y2 = str(self.r2[1])
        z2 = str(self.r2[2])

        return '*TRANSFORM, NSET=' + self.nset.name + ', TYPE=' + self.typetransform + '\n' \
            +  x1 + ',' + y1 + ',' + z1 + ',' + x2 + ',' + y2 + ',' + z2 + '\n'
    

def read(name,content,new_cards):

    # *TRANSFORM, NSET=BOT, TYPE=C
    # 0,0,0,0,0,1

    name = name.upper() # name = *TRANSFORM, NSET=bot, TYPE=C
    content = content[0].replace('\n','') # content = '0,0,0,0,0,1'
    
    nset_name = name.split(',')[1].split('=')[1] # nset = 'bot'

    try:
        nset = [ icard for icard in new_cards if icard.name == nset_name][0]
        # este debe set una instancia de NsetCard o NsetCardofNset
        # comprobar
        
    except:
        raise Exception('Nset not found: ' + nset_name)

    r12 = content[0].split(',') # r1 = ['0', '0', '0', '0', '0', '1']
    r12 = [float(i) for i in r12] # r1 = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

    r1 = r12[:3] # r1 = [0.0, 0.0, 0.0]
    r2 = r12[3:] # r2 = [0.0, 0.0, 1.0]

    # numpy array
    r1 = np.array(r1)
    r2 = np.array(r2)

    type = name.split(',')[2].split('=')[1] # type = 'C'
    return TransformCard(nset,r1,r2,type)