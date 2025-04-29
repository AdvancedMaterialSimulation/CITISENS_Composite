import numpy as np
import pandas as pd
from djccx.inp.cards.Card import Card
from djccx.inp.cards.NodeCard import NodeCard
from matplotlib import pyplot as plt
from random import randint
from djccx.tools.el2face import el2face

# =============================================================================
class ElementCard(Card):
    def __init__(self, name, content,verbose=False):
        super().__init__(name, content)
        self.type = '*ELEMENT'
        # append the data
        data = content
        # remove \n
        data = [data.replace('\n', '').split(',') for data in data]
        
        if data[-1] == ['']:
            data = data[:-1]
        # to float
        data = [[int(data) for data in data] for data in data]
        data = np.array(data)

        self.eid = data[:, 0]
        self.elements = data[:, 1:]
        self.df = pd.DataFrame(self.elements, index=self.eid)

        if self.options["TYPE"] in ["C3D10", "C3D10MH"]:
            self.dimension = 3
            self.options["TYPE"] = "C3D10"
            self.name = self.name.replace("C3D10MH", "C3D10")
        elif self.options["TYPE"] in ["CPS6", "CPE6"]:
            self.dimension = 2
            self.options["TYPE"] = "CPS6"
            self.name = self.name.replace("CPE6", "CPS6")
        elif self.options["TYPE"] == "T3D3":
            self.dimension = 1
        else:
            self.dimension = -1
            if verbose:
                print("TYPE: ", self.options["TYPE"])
                print("ERROR: Element type not implemented")

        # if doesn't have ELSET, the name must ELSET_NAME
        if "ELSET" not in self.options.keys():
            number = randint(0, 100000)
            num_str_6 = str(number).zfill(6)
            self.options["ELSET"] = "ELSET_NAME_" + num_str_6 
            self.name = self.options["ELSET"] 
        self.name = self.options["ELSET"]
        self.Nodes = None
        self.UniqueNodes = None

    # =============================================================================
    def SetNodes(self, nodes):
        self.Nodes = self.GetNodes(nodes)
        self.UniqueNodes = self.GetUniqueNodes(nodes)
        return self
    # =============================================================================

    def GetNodes(self, nodes):
        # nodes must be a NodeCard
        assert type(nodes) == NodeCard, "nodes must be a NodeCard"
        # get the nodes

        element_nodes = [nodes.df.loc[element] for element in self.elements]

        return element_nodes
    # =============================================================================

    def GetUniqueNodes(self, nodes):
        elements_flat = self.elements.flatten()
        unique_elements = np.unique(elements_flat)

        return nodes.df.loc[unique_elements]
    
    def GetUniqueNodesTetra(self, nodes):
        elements_flat = self.elements[:,0:4].flatten()
        unique_elements = np.unique(elements_flat)

        return nodes.df.loc[unique_elements]
    # =============================================================================

    def GetMassCenter(self, nodes):
        # get the nodes
        if self.UniqueNodes is None:
            self.UniqueNodes = self.GetUniqueNodes(nodes)
        if self.Nodes is None:
            self.Nodes = self.GetNodes(nodes)

        # get the mass center
        mass_center = np.mean(self.UniqueNodes[['x', 'y', 'z']], axis=0)
        # to array
        mass_center = np.array(mass_center)
        return mass_center
    # =============================================================================

    def GetSTD(self, nodes):
        # get the nodes
        if self.UniqueNodes is None:
            self.UniqueNodes = self.GetUniqueNodes(nodes)
        # get the mass center
        std = np.std(self.UniqueNodes[['x', 'y', 'z']], axis=0)
        # to array
        std = np.array(std)
        # mean
        std = np.mean(std)
        return std
    
    # =============================================================================
    def GetDiameter(self, nodes):

        mass_center = self.GetMassCenter(nodes)
        # get the nodes
        if self.UniqueNodes is None:
            self.UniqueNodes = self.GetUniqueNodes(nodes)
        # get the mass center
        # distance
        distance = np.linalg.norm(self.UniqueNodes[['x', 'y', 'z']] - mass_center, axis=1)
        # max distance
        diameter = np.max(distance)
        return diameter
    # =============================================================================

    def plot(self, nodes, *args, **kwargs):
        # get the nodes
        nodes = self.GetUniqueNodes(nodes)
        # plot
        plt.plot(nodes["x"], nodes["y"], *args, **kwargs)

    def plot3D(self, ax,nodes, *args, **kwargs):
        # get the nodes
        nodes = self.GetUniqueNodesTetra(nodes)
        # plot
        ax.plot3D(nodes["x"].values, nodes["y"].values,
                  nodes["z"].values, *args, **kwargs)

    def restart_index_nodes(self, id_node_start):
        self.elements = self.elements + id_node_start
        self.df = pd.DataFrame(self.elements, index=self.eid)

        return self

    def restart_index_element(self, id_el_start):
        self.eid = self.eid + id_el_start
        self.df = pd.DataFrame(self.elements, index=self.eid)

        return self

    def print(self):
        return "*ELEMENT, TYPE=" + \
            self.options["TYPE"] + \
                ", ELSET=" +\
            self.name + "\n"+self.df.to_csv(index=True, header=False)

    def merge(self, el2):
        self.content = self.content + el2.content
        self.eid = np.concatenate([self.eid, el2.eid])
        self.elements = np.concatenate([self.elements, el2.elements])
        self.df = pd.DataFrame(self.elements, index=self.eid)
        return self


    def select_faces(element,all_elements,nodes):

        nodes = nodes.copy()
        nodes["real_index"] = np.arange(0,len(nodes))
        
        all_faces = []


        ide     = element.eid
        el_data = all_elements.loc[ide]
        
        el_data = el_data[[0,1,2,3]]

        el_data_real_index = [ nodes.loc[el_data.iloc[i].values].real_index.values 
                            for i in range(len(el_data))]

        for i in range(len(el_data_real_index)):
            faces = el2face(el_data_real_index[i])
            all_faces.extend(faces)

        return all_faces