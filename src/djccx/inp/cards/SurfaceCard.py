from djccx.inp.cards.Card import Card
from djccx.inp.cards.NsetCard import NsetCard
from djccx.inp.cards.ElsetCard import ElsetCard
from djccx.tools.el2face import el2face

import numpy as np
import pandas as pd

class SurfaceCard (Card):
    def __init__(self, name, elsets):
        super().__init__(name, elsets)

        self.elsets = elsets
        self.type = '*SURFACE'

    def print(self):
        line = ''
        for i, elset in enumerate(self.elsets):
            if len(elset.id_elements) == 0:
                continue
            # last 
            line += str(elset.name) + ',S' + str(i+1) + '\n' 
        line = line[:-1]
        return self.type + ', NAME=' + self.name_up  +",TYPE=ELEMENT"+ '\n' + line 
    
    def select_faces(surf,all_elements,nodes): 
        """   
        Inputs:
        -------
        * inp_obj: object of class Inp
        * surf: object of class Surface
        * elem: object of class Element
        * nodes: object of dataframe nid,x,y,z
        """

        nodes = nodes.copy()
        nodes["real_index"] = np.arange(0,len(nodes))

        all_faces = []
        for k in range(4):
            elset = surf.elsets[k]

            ide     = elset.id_elements
            el_data = all_elements.loc[ide]
            
            el_data = el_data[[0,1,2,3]]

            el_data_real_index = [ nodes.loc[el_data.iloc[i].values].real_index.values 
                                for i in range(len(el_data))]

            for i in range(len(el_data_real_index)):
                faces = el2face(el_data_real_index[i],nface=k)
                all_faces.extend(faces)

        return all_faces

# =============================================================================
class SurfaceNodeCard (Card):
    def __init__(self, name, nset):
        super().__init__(name, nset)

        self.nset = nset
        self.type = '*SURFACE'

    def print(self):
        # print the nodes but only in row of 10
        return self.type    + ', NAME=' +\
               self.name_up + ',TYPE=NODE\n' +\
               self.nset.name 

    def restart_index_element(self, id_elements):
        self.id_elements = self.id_elements + id_elements

        return self

# =============================================================================


def read(name,content,new_cards,verbose=False):

    printw = lambda x: print(x) if verbose else None

    name_surf = name.replace("*SURFACE,","")
    opt_surf = name_surf.split(",")
    opt_surf = [i.split("=") for i in opt_surf]
    opt_surf = {i[0]:i[1] for i in opt_surf}

    name_surf = opt_surf["NAME"]
    ncontent = content[0].replace("\n","").replace(" ","")

    if opt_surf["TYPE"] != "ELEMENT":
        
        nset = [ icard for icard in new_cards
                    if isinstance(icard,NsetCard)
                    if icard.name == ncontent]
        if len(nset) == 0:
            printw("No existe nset: "+ncontent)
            return None
        if len(nset) > 1:
            printw("Existe mas de un nset: "+ncontent)
            return None
        nset = nset[0]
        new_card = SurfaceNodeCard(name_surf,nset)

    else:
        csurf = [i.replace("\n","") for i in content]
        csurf = [i.split(",") for i in csurf]
        csurf = {i[1]:i[0] for i in csurf}

        surf_elset  = []
        for i in range(1,5):
            if "S"+str(i) not in csurf.keys():
                string ="_".join(csurf[list(csurf.keys())[0]].split("_")[:-1])
                string = string  + "_"+str(i)
                csurf["S"+str(i)] = string
            surfaces_el = [ icard for icard in new_cards 
                    if isinstance(icard,ElsetCard)
                    if icard.name == csurf["S"+str(i)]]
            if len(surfaces_el) == 0:
                printw("No existe elset: "+csurf["S"+str(i)])
                continue
            if len(surfaces_el) > 1:
                printw("Existe mas de un elset: "+csurf["S"+str(i)])
                continue
            surf_elset.append(surfaces_el[0])
        new_card = SurfaceCard(name_surf,surf_elset)
    
    return new_card