

from djccx.inp.CreateCards.CreatePBC_with_tie             import CreatePBC_with_tie
from djccx.inp.CreateCards.AddEquation                    import AddEquation
from djccx.inp.CreateCards.Nset.CreateNsetFromElement     import CreateNsetFromElementIndex,CreateNsetFromElement
from djccx.inp.CreateCards.Surface.CreateSurfNodeFromNset import CreateSurfNodeFromNset
from djccx.inp.CreateCards.Nset.CreateNsetFromIds         import CreateNsetFromIds
from djccx.inp.CreateCards.CreateElsetAll                 import CreateElsetAll
from djccx.inp.CreateCards.Nset.CreateNsetFromLabels      import CreateNsetFromLabels
from djccx.inp.CreateCards.Nset.CreateNsetFromNsets       import CreateNsetFromNsets
from djccx.inp.CreateCards.CreateContacts                 import CreateContacts
from djccx.inp.CreateCards.Nset.CreateNsetCopy            import CreateNsetCopy
from djccx.inp.CreateCards.Nset.CreateCopyNset            import CreateCopyNset
from djccx.inp.CreateCards.CreateTie                      import CreateTie
from djccx.inp.CreateCards.CreateSolidSection             import CreateSolidSection
from djccx.inp.CreateCards.Nset.CreateSkeletonFromTrajs   import CreateSkeletonFromTrajs
from djccx.inp.CreateCards.Surface.CreateSurfaceFromNset  import CreateSurfaceFromNset
from djccx.inp.CreateCards.CreateElasticMaterial          import CreateElasticMaterial
from djccx.inp.CreateCards.CreateElasticEngineeringMaterial import CreateElasticEngineeringMaterial
from djccx.inp.CreateCards.CreateStaticStep               import CreateStaticStep
from djccx.inp.CreateCards.CreateTransform                import CreateTransform
from djccx.inp.CreateCards.CreateShellSection             import CreateShellSection
from djccx.inp.CreateCards.CreateOrientation              import CreateOrientation
from djccx.inp.CreateCards.CreateElsetFromElsets          import CreateElsetFromElsets
from djccx.inp.CreateCards.CreateNsetFromElset            import CreateNsetFromElset

class AbstractCreate:

    # ===========================================
    def CreateNsetFromIds(self,id_values_list,name=None):
        return CreateNsetFromIds(self,id_values_list,name=name)
    # ===========================================
    def CreateSurfNodeFromNset(self,id_values_list,name=None):
        return CreateSurfNodeFromNset(self,id_values_list,name=name)
    # ===========================================
    def AddEquation(self,nset1,nset2,type_eq="point2point",dims=[1,2,3],nodes=None):
        return AddEquation(self,nset1,nset2,type_eq=type_eq,dims=dims,nodes=nodes)
    # ===========================================
    def CreateNsetFromElementIndex(self,index_el,name=None):
        return CreateNsetFromElementIndex(self,index_el,name=name)
    # ===========================================
    def CreateNsetFromElement(self,element,name):
        return CreateNsetFromElement(self,element,name)
    # ===========================================
    def CreateTie(self,name,slave,master,type="surface"):
        return CreateTie(self,name,slave,master,type=type)
    # ===========================================    
    def CreateCopyNset(self,nameset,nameset_copy,vec):
        return CreateCopyNset(self,nameset,nameset_copy,vec)
    # ===========================================
    def CreatePBC_with_tie(self,tie_name,nset,surface,vec):
        return CreatePBC_with_tie(self,tie_name,nset,surface,vec)
    # ===========================================
    def CreateSolidSection(self,elset,material,orientation=None):
        return CreateSolidSection(self,elset,material,orientation=orientation)
    # =================================
    def CreateNsetCopy(inp_file,rep_nset,label,vec):
        return CreateNsetCopy(inp_file,rep_nset,label,vec)
    # =================================
    def CreateElsetAll(self):
        return CreateElsetAll(self)
    # ================================= 
    def CreateNsetFromLabels(inp_file,name,labels):
        return CreateNsetFromLabels(inp_file,name,labels)
    # =================================
    def CreateNsetFromNsets(inp_file,name,nsets):
        return CreateNsetFromNsets(inp_file,name,nsets)
    # =================================
    def CreateContacts(inp_file,contacts):
        return CreateContacts(inp_file,contacts)
    # =================================
    def CreateSkeletonFromTrajs(inp_files,element,trajs,radius=0.2,name="esqueleto"):
        return CreateSkeletonFromTrajs(inp_files,element,trajs,radius=radius,name=name)
    # =================================
    def CreateSurfaceFromNset(self,name,nset):
        return CreateSurfaceFromNset(self,name,nset)
    # =================================
    def CreateElasticMaterial(self,name,E,nu):
        return CreateElasticMaterial(self,name,E,nu)
    # =================================
    def CreateElasticEngineeringMaterial(self,name,E1,E2,E3,nu12,nu13,nu23,G12,G13,G23):
        return CreateElasticEngineeringMaterial(self,name,E1,E2,E3,nu12,nu13,nu23,G12,G13,G23)
    # =================================
    def CreateStaticStep(self,nlgeom=False):
        return CreateStaticStep(self,nlgeom=nlgeom)
    # =================================
    def CreateTransform(self,nset,r1,r2):
        return CreateTransform(self,nset,r1,r2)
    # =================================
    def CreateOrientation(self,name,a,b):
        return CreateOrientation(self,name,a,b)
    
    # =================================
    def CreateShellSection(self,elset,material):
        return CreateShellSection(self,elset,material)
    
    # =================================
    def CreateElsetFromElsets(self,elsets,name):
        return CreateElsetFromElsets(self,elsets,name)
    
    # =================================
    def CreateNsetFromElset(self,elset,name=None):
        return CreateNsetFromElset(self,elset,name=name)