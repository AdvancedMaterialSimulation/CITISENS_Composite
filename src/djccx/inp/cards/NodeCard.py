from djccx.inp.cards.Card import Card
import os
import pandas as pd

class NodeCard (Card):
    def __init__(self, name, content):
        super().__init__(name, content)
        self.nid = []
        self.x = []
        self.y = []
        self.z = []
        self.type = '*NODE'


        # write all lines to a file in one step
        with open('temp_nodes.txt', 'w') as f:
            f.writelines(self.content)
        # read as csv
        self.df = pd.read_csv('temp_nodes.txt', sep=',', header=None,
                        names=['nid', 'x', 'y', 'z'])
        # nid can be a index
        self.df.set_index('nid', inplace=True)
        # nid can be a index

        # remove temp file
        os.remove('temp_nodes.txt')


    def print(self):

        return self.name +\
              "\n" +self.df.to_csv(index=True,header=False,float_format='%.10f')
    
