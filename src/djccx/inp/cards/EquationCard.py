from djccx.inp.cards.Card import Card
import numpy as np
class EquationCard(Card):
    def __init__(self, name, nset1, nset2, 
                 type_eq="point2point", 
                 nodes=None,
                 dims=[1,2,3]):
        super().__init__(name, name)

        self.nset1 = nset1
        self.nset2 = nset2
        self.type_eq = type_eq
        self.type = '*EQUATION'
        self.nodes =nodes
        self.dims = dims


    def print(self):
        if self.type_eq == "point2point":
            return self.print_point()
        elif self.type_eq == "mean":
            return self.print_mean()
        elif self.type_eq == "zmirror":
            return self.print_zmirror()
        elif self.type_eq == "zmirror_point":
            return self.print_zmirror_point()
        elif self.type_eq == "set_center_mass":
            return self.print_set_center_mass()
        elif self.type_eq == "linear_interpolation":
            return self.print_linear_interpolation()
        
    def print_point(self):
        # print the nodes but only in row of 10
        initial_coment = "** This equation is for the nodes in the nset1 and nset2\n"
        # name of nset1 and nset2
        initial_coment = initial_coment + "** nset1: {}\n".format(self.nset1.name)
        initial_coment = initial_coment + "** nset2: {}\n".format(self.nset2.name)
        initial_coment = initial_coment + "** type_eq: {}\n".format(self.type_eq)
        initial_coment = initial_coment + "** dims: {}\n".format(self.dims)
        initial_coment = initial_coment + "************************\n"
        line_eq = ""
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes
        # comprobar que tienen el mismo numero de nodos
        if len(id_1) != len(id_2):
            print("ERROR: EquationCard:print_point: nset1 and nset2 have different number of nodes")
            return None
        for j,k in zip(id_1,id_2):
            for dim in self.dims:
                line_eq = line_eq +\
                      "2\n{} , {} , 1 , {} , {} , -1\n".format(j,dim,k,dim)


        return initial_coment + self.type + '\n' + line_eq 


    def print_mean(self):
        # print the nodes but only in row of 10
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes
        nterm = len(id_1) + len(id_2)
        
        line_eq_total = ""
        for dim in self.dims:
            line_eq = "*EQUATION\n"+str(nterm) + '\n'
            for i1 in id_1:
                line_eq = line_eq + "{} , {} ,  {},\n".format(i1,dim,1/len(id_1))    
            for i2 in id_2:
                line_eq = line_eq + "{} , {} , -{},\n".format(i2,dim,1/len(id_2))
        # remove last comma
            line_eq = line_eq[:-2] + '\n'
            line_eq_total = line_eq_total + line_eq
        line_eq_total = line_eq_total[:-1]
        return line_eq_total
    
    def print_zmirror_point(self):
        # print the nodes but only in row of 10
        line_eq = ""
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes
        # comprobar que tienen el mismo numero de nodos
        if len(id_1) != len(id_2):
            print("ERROR: EquationCard:print_point: nset1 and nset2 have different number of nodes")
            return None
        for j,k in zip(id_1,id_2):
            for dim in self.dims:
                sign = "" if dim == 3 else "-"
                line_eq = line_eq +\
                      "2\n{} , {} , 1 , {} , {} , {}1\n".format(j,dim,k,dim,sign)


        return self.type + '\n' + line_eq 
    def print_zmirror(self):
        # print the nodes but only in row of 10
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes
        nterm = len(id_1) + len(id_2)
        
        line_eq_total = ""
        for dim in  [1,2,3]:
            line_eq = "*EQUATION\n"+str(nterm) + '\n'
            for i1 in id_1:
                line_eq = line_eq + "{} , {} ,  {},\n".format(i1,dim,1/len(id_1))
            sign = "" if dim == 3 else "-"     
            for i2 in id_2:
                line_eq = line_eq + "{} , {} , {}{},\n".format(i2,dim,sign,1/len(id_2))
        # remove last comma
            line_eq = line_eq[:-2] + '\n'
            line_eq_total = line_eq_total + line_eq
        line_eq_total = line_eq_total[:-1]
        return line_eq_total
    
    def print_set_center_mass(self):
        # print the nodes but only in row of 10
        id_1 = self.nset1.id_nodes
        nterm = len(id_1) 
        
        line_eq_total = ""
        for dim in self.dims:
            line_eq = "*EQUATION\n"+str(nterm) + '\n'
            for i1 in id_1:
                line_eq = line_eq + "{} , {} ,  1,\n".format(i1,dim)

        # remove last comma
            line_eq = line_eq[:-2] + '\n'
            line_eq_total = line_eq_total + line_eq
        line_eq_total = line_eq_total[:-1]
        return line_eq_total
        
    def print_linear_interpolation(self):
        # print the nodes but only in row of 10
        # nodes must be defined
        if self.nodes is None:
            print("ERROR: EquationCard:print_linear_interpolation: nodes must be defined")
            raise ValueError("nodes must be defined")
        
        nodes = self.nodes # dpandas dataframe with the nodes
        id_1 = self.nset1.id_nodes
        id_2 = self.nset2.id_nodes

        nodes_1 = nodes.loc[id_1]
        nodes_2 = nodes.loc[id_2]
        line_eq = "" 

        npoints = 5
        for i in range(len(id_1)):
            node_1 = nodes_1.loc[id_1[i]].values
            
            # find the two closest nodes in nodes_2
            distances = np.linalg.norm(nodes_2 - node_1,axis=1)
            # select 2 closest nodes
            id_closest = np.argsort(distances)[:npoints]
            # select de distances of the closest nodes
            distances = distances[id_closest]
            #
            id_closest = id_2[id_closest]
            # if some distance is 0 change by 1e-6
            distances[distances == 0] = 1e-8
            # calculate the weights
            weights = 1/distances
            # normalize the weights
            weights = weights/np.sum(weights)
            # noew the equation is the linear interpolation
            # nodes_1 - w1*node_1 + w2*node_2 = 0
            for dim in self.dims:
                replace_stt = [id_1[i],dim]
                
                id_dim_w = [ [i_id_cl,dim,w] for i_id_cl,w in zip(id_closest,weights)]

                replace_stt = replace_stt + [i for sublist in id_dim_w for i in sublist]


                line_eq = line_eq +\
                            "{}\n{},{},1  ,  {},{},-{}  ,  {},{},-{}  \n".format(npoints+1,*replace_stt)
        return self.type + '\n' + line_eq
    def restart_index_nodes(self, id_node_start):
        self.id_nodes = self.id_nodes + id_node_start

        return self
