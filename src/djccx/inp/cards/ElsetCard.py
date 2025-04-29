from djccx.inp.cards.Card import Card
import numpy as np
import pandas as pd
from djccx.tools.el2face import el2face

class ElsetCard (Card):
    def __init__(self, name, id_elements):
        super().__init__(name, id_elements)

        self.id_elements = id_elements
        self.type = '*ELSET'

    def print(self):
        # print the nodes but only in row of 10
        line = ''
        for i, element in enumerate(self.id_elements):
            line += str(element) + ','
            if i % 10 == 0 and i != 0:
                line += '\n'
        line = line[:-1]
        return self.type + ', ELSET=' + self.name_up + '\n' + line 

    def restart_index_element(self, id_elements):
        self.id_elements = self.id_elements + id_elements

        return self

    def select_faces(elset,all_elements,nodes):

        nodes = nodes.copy()
        nodes["real_index"] = np.arange(0,len(nodes))
        
        all_faces = []


        ide     = elset.id_elements
        el_data = all_elements.loc[ide]
        
        el_data = el_data[[0,1,2,3]]

        el_data_real_index = [ nodes.loc[el_data.iloc[i].values].real_index.values 
                            for i in range(len(el_data))]

        for i in range(len(el_data_real_index)):
            faces = el2face(el_data_real_index[i])
            all_faces.extend(faces)

        return all_faces
    
    # =============================================================================

    def GetUniqueNodes(self, inp_f):

        volumes = [ iv for iv in inp_f.elements 
                       if iv.dimension == 3]
        df_el_all = [ volumes[i].df 
                     for i in range(len(volumes)) ]
        df_el_all = pd.concat(df_el_all)

        elements_flat = self.id_elements.flatten()
        unique_elements = np.unique(elements_flat)

        df_el = df_el_all.loc[unique_elements]
        df_el = df_el.values.flatten()
        df_el = np.unique(df_el)

        nodes = inp_f.nodes

        return nodes.df.loc[df_el]
    
class ElsetofElsetCard (Card):
    def __init__(self, name, id_elements):
        super().__init__(name, id_elements)

        self.id_elements = id_elements
        self.type = '*ELSETOFELSET'

    def print(self):
        # print the nodes but only in row of 10
        line = ''
        for i, element in enumerate(self.id_elements):
            line += str(element) + ','
            if i % 10 == 0 and i != 0:
                line += '\n'
        line = line[:-1]
        return '*ELSET, ELSET=' + self.name_up + '\n' + line 



def read(content,name):
    c = "".join(content)
    c = c.replace('\n','')
    c = c.split(',')
    if c[-1] == '':
        c = c[:-1]
    name = name.replace("\n","").split("ELSET=")[-1]

    try:
        # 
        c_proc = c
        # remove empty spaces
        c_proc = [i.replace(" ","") for i in c_proc]
        # if some element is "" remove it
        c_proc = [i for i in c_proc if i != ""]
        c_proc = np.array(c_proc,dtype=int)
        new_card = ElsetCard(name,c_proc)
    except:
        new_card = ElsetofElsetCard(name,c)

    return new_card