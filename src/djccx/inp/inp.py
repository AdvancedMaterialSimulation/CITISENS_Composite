from djccx.inp.cards.Card import *
import numpy  as np

from djccx.inp.init                   import init

from djccx.inp.transformations.SetUniqueNodes         import SetUniqueNodes
from djccx.inp.transformations.addDisplFRD            import addDisplFRD
from djccx.inp.transformations.addDisplacement        import addDisplacement

from djccx.inp.basic.merge                  import merge
from djccx.inp.basic.print                  import print
from djccx.inp.basic.select                 import *
from djccx.inp.basic.SetPrefix              import SetPrefix
from djccx.inp.basic.setResults             import setResults
from djccx.inp.basic.setResultsSteps        import setResultsSteps
from djccx.inp.basic.filter_by_type         import filter_by_type
from djccx.inp.basic.remove_lib             import *
from djccx.inp.basic.plots                  import *
from djccx.inp.basic.remove_by_type         import remove_by_type
from djccx.inp.basic.GetNodesElement        import GetNodesElement
from djccx.inp.basic.reset_index            import reset_index

from djccx.inp.CreateCards.AbstractCreate import AbstractCreate

from djccx.inp.frd2json import frd2json
from djccx.inp.inp2json import inp2json
from djccx.plot.plotlyinpdata import plotlyinpdata
import plotly.graph_objects as go
from djccx.runccx import runccx
import os,shutil
from djccx.frd.readfrd import readfrd
from djccx.plot.plotly import plotly as plotlyfrd
import pandas as pd

join = os.path.join
filter = lambda self,type: [card for card in self.cards if card.type == type]

opt_default = {
    "OMP_NUM_THREADS":4,
    "mpi_np":4,
    "mpi":True
}
# ===========================================

class inp(AbstractCreate):

    def __init__(self, 
                 file_name:str      ,
                 warning  :bool=True):
        init(self,file_name,warning)
    # ===========================================
    @property
    def nodes(self):
        return filter(self,"*NODE")[0]
    
    @property
    def elements(self):
        return filter(self,"*ELEMENT")
    
    @property
    def nsets(self):
        return filter(self,"*NSET")
    
    @property
    def elsets(self):
        return filter(self,"*ELSET")
    
    @property
    def elsetsofelsets(self):
        return filter(self,"*ELSETOFELSET")
    
    @property
    def surfaces(self):
        return filter(self,"*SURFACE")
    
    @property
    def ties(self):
        return filter(self,"*TIE")
    
    @property
    def equations(self):
        return filter(self,"*EQUATION")
    
    @property
    def surface_interactions(self):
        return filter(self,"*SURFACEINTERACTION")
    
    @property
    def contacts(self):
        return filter(self,"*CONTACTPAIR")
    
    @property
    def materials(self):
        return filter(self,"*MATERIAL")
    
    @property
    def solid_sections(self):
        return filter(self,"*SOLIDSECTION")
    
    @property
    def shell_sections(self):
        return filter(self,"*SHELLSECTION")
    
    @property
    def steps(self):
        return filter(self,"*STEP")
    
    @property
    def transforms(self):
        return filter(self,"*TRANSFORM")
    
    @property
    def orientations(self):
        return filter(self,"*ORIENTATION")


    # ===========================================
    def GetNodesElement(self,element):
        return GetNodesElement(self,element)
    # ===========================================
    def plot(self,*args,**kwargs):
        plot(self,*args,**kwargs)
    # ===========================================
    def plot3D(self,ax,*args,**kwargs):
        plot3D(self,ax,*args,**kwargs)
    # ===========================================
    def filter_by_type(self,
                       dim,
                       replace:bool=False) -> list:
        return filter_by_type(self,dim,replace=replace)
    # ===========================================   
    def remove_by_type(self,dim):
        return remove_by_type(self,dim)
    # ===========================================        
    def last_node_id(self):
        return max(self.nodes.df.index)
    # ===========================================
    def last_element_id(self):
        all_el = [element.eid for element in self.elements]
        all_el = np.concatenate(all_el)
        return np.max(all_el)
    # ===========================================
    def reset_index(self,last_node_id,last_ele_id):
        return reset_index(self,last_node_id,last_ele_id)
    # ===========================================
    def merge(self,inp2,prefix=""):
        return merge(self,inp2,prefix)
    # ===========================================
    def print(self, file="test.inp",inline=False):
        return print(self,file=file,inline=inline)
    # ===========================================    
    def SetUniqueNodes(inp_f):
        return SetUniqueNodes(inp_f)
    # ===========================================
    def remove_nset(self,name):
        return remove_nset(self,name)
    # ===========================================
    def remove_surface(self,name):
        return remove_surface(self,name)
    # ===========================================
    def remove_surface_regex(self,regex):
        remove_surface_regex(self,regex)
    # ===========================================
    def remove_nset_regex(self,regex):
        remove_nset_regex(self,regex)
    # ===========================================
    def remove_tie(self,name):
        remove_tie(self,name)
    def remove_tie_regex(self,regex):
        remove_tie_regex(self,regex)
    # ===========================================
    def select(self,name,type):
        return select(self,name,type)
    # ===========================================
    def select_regex(self,regex,type):
        return select_regex(self,regex,type)
    # ===========================================
    def addDisplacement(self,vec):
        addDisplacement(self,vec)
    # ===========================================  
    def addDisplFRD(self,frd):
        return addDisplFRD(self,frd)
    # =================================
    def setResults(self,frd,onlyfrd=False):
        return setResults(self,frd,onlyfrd=onlyfrd)
    # =================================
    def setResultsSteps(self,frd,onlyfrd=False):
        return setResultsSteps(self,frd,onlyfrd=onlyfrd)
    # =================================    
    def scale(self,factor):
        self.nodes.df[["x","y","z"]] = self.nodes.df[["x","y","z"]]*factor
        return self
    # =================================
    def SetPrefix(self,prefix):
        return SetPrefix(self,prefix)
    # =================================
    def frd2json(self,frd=None,elements=None):
        return frd2json(self,frd=frd,elements=elements)
    
    def inp2json(self,elements=None):
        return inp2json(self,elements=elements)
    
    def in2jsonarray(self,elements=None):
        elements = self.elements if elements is None else elements
        return [ inp2json(self,elements=[element]) for element in elements]
    
    def plotly(self,elements=None):
        
        json_data = self.in2jsonarray(elements)
        data = [plotlyinpdata(ijson) for ijson in json_data]

        fig = go.Figure(data=data)
        # legend
        fig.update_layout(legend_title_text='Element Sets')
        fig.update_layout(width=500, height=500)

        fig.show()

    def plotlyfrd(self,clim=None,elements=None):
        if self.frd is None:
            raise Exception("FRD file not found, please run the simulation first")
        json_data = self.frd2json(elements=elements)
        plotlyfrd(json_data,clim=clim)


    def matplotlib(self,fig=None):
        fig = plt.figure() if fig is None else fig
        ax = fig.add_subplot(111, projection='3d')

        nodes = self.nodes
        elements = self.elements
        ncolors = len(elements)
        colors = plt.cm.hsv(np.linspace(0,1,ncolors))
        for i,iel in enumerate(elements):
            iel.plot3D(ax,nodes, color=colors[i],
                    alpha=0.8,linestyle="none",marker=".",label=iel.name)
        # aspect ratio
        xlim = ax.get_xlim()
        xlen = xlim[1] - xlim[0]
        ylim = ax.get_ylim()
        ylen = ylim[1] - ylim[0]
        zlim = ax.get_zlim()
        zlen = zlim[1] - zlim[0]

        ax.set_box_aspect([xlen/zlen, ylen/zlen, 1])

        # legend 
        plt.legend( bbox_to_anchor=(1.05, 1), loc='upper left')

    def run(self,output,mkdirforce=False,opt=opt_default):
        
        exist = os.path.exists(output)
        if exist:
            shutil.rmtree(output)
            os.mkdir(output)
        else:
            if mkdirforce:
                os.mkdir(output)
            else:
                raise Exception(f"Directory {output} does not exist")
            
        file = join(output,"main.inp")
        self.print(file=file)



        runccx(output,"main",**opt)

        frd_file = join(output,"main.frd")

        frd = readfrd(frd_file)

        self.setResults(frd)

        return frd
    
    def cleansteps(self):
        
        self.cards = [card for card in self.cards if card.type != "*STEP"]

        # clean results

        self.frd = None

    def contactdataframe(self):
        
        contacts_name = [contact.name for contact in self.contacts]
        slave = [contact.slave.name for contact in self.contacts]
        master = [contact.master.name for contact in self.contacts]

        cols = ["name","slave","master"]
        df = pd.DataFrame({
            "name": contacts_name,
            "slave": slave,
            "master": master
        })

        # sort by slave
        df = df.sort_values(by="slave")

        return df
    
